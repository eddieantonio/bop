#!/usr/bin/env python
# coding: utf-8

# Copyright 2016 Eddie Antonio Santos <easantos@ualberta.ca>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Includes the Parser.
"""

import re

from itertools import takewhile
from .utils import dedefaultdictize, vivify

KEY_PATTERN = re.compile(r"""
    \[
        (
            [^\]]*  # Capture anything within square brackets.
        )
    \]
""", re.VERBOSE)

WEIGHT_PATTERN = re.compile("""
    (.+),   # Anything, up to a comma
    \s+
    (
        [^,]+ # Capture anything BUT a comma
    )
    $ # And it must match at the end of the line.
""", re.VERBOSE)


class Parser(object):
    """
    Used internally to parse Boa output and produce decent results.
    """
    def __init__(self, weighted=False):
        self.weighted = weighted
        self.buffer = []
        self.new_value_pattern = None
        self._container = None

    @property
    def result(self):
        if self._container is None:
            raise RuntimeError('Container type not yet determined '
                               '(parse at least one line of input)')
        self.finalize()
        return dedefaultdictize(self._container)

    @property
    def initialized(self):
        return (self._container is not None and
                self.new_value_pattern is not None)

    def add_result(self, *args):
        assert len(args) >= 2
        keys, value = args[:-1], args[-1]

        if isinstance(self._container, list):
            self._container.append(value)
            return self

        current_dict = self._container
        for key in keys[:-1]:
            current_dict = current_dict[key]
        current_dict[keys[-1]] = value

        return self

    @staticmethod
    def parse_weight(string):
        assert not string.endswith('\n')
        match = WEIGHT_PATTERN.search(string)
        assert match
        return match.group(1, 2)

    def ingest(self, text):
        """
        Ingest arbitrary text and add it to the buffer
        """

        # Just adding text with out a new line to the buffer.
        if len(self.buffer) > 0 and '\n' not in text:
            self.buffer[-1] += text
            return

        if not self.initialized:
            self.detect_format(text)

        if text == '\n':
            self.buffer += ''
            return self

        portions = text.split('\n')
        this_line, next_line = self.segregate(portions)

        while len(next_line) > 0:
            if len(this_line) == 0:
                self.finalize()
                this_line, next_line = next_line, None
                break
            else:
                self.buffer += this_line
                self.finalize()
            this_line, next_line = self.segregate(next_line)

        self.buffer += this_line
        return self

    def finalize(self):
        if not len(self.buffer):
            return
        self.parse_line('\n'.join(self.buffer))
        self.buffer = []

    def segregate(self, portions):
        """
        Returns lists of this line and the rest of the lines.

        >>> parser = Parser().detect_format('var[] = herp')
        >>> parser.segregate(['herp', '', 'derp', 'var[] = herp'])
        (['herp', '', 'derp'], ['var[] = herp'])
        >>> parser.segregate(['var[] = herp'])
        ([], ['var[] = herp'])
        """
        def is_not_line_start(p):
            return not self.new_value_pattern.match(p)
        this_line = list(takewhile(is_not_line_start, portions))
        rest = portions[len(this_line):]
        return this_line, rest

    def parse_line(self, raw_line):
        """
        >>> Parser().parse_line('foo[] = bar').result
        ['bar']
        """
        line = raw_line.rstrip('\n')
        if not self.initialized:
            self.detect_format(line)

        keys_string, value = self.cleave(line)
        _, keys = self.parse_keys(keys_string)
        assert len(keys) > 0

        # Remove the "dummy" empty key for lists and weighted results.
        if isinstance(self._container, dict) and keys[-1] == '':
            keys.pop()

        if self.weighted:
            final_key, weight = self.parse_weight(value)
            self.add_result(*(keys + [final_key, weight]))
        else:
            self.add_result(*(keys + [value]))
        return self

    @staticmethod
    def parse_keys(keys_string):
        """
        >>> Parser().parse_keys('counts[foo][bar]')
        ('counts', ['foo', 'bar'])
        >>> Parser().parse_keys('counts[]')
        ('counts', [''])
        """
        parsed = KEY_PATTERN.split(keys_string)
        assert len(parsed) > 1
        # Results are in every SECOND item.
        return parsed[0], parsed[1::2]

    def detect_format(self, line):
        r"""
        >>> Parser().result
        Traceback (most recent call last):
            ...
        RuntimeError: Container type not yet determined ...
        >>> parser = Parser().detect_format('counts[] = Herp')
        >>> isinstance(parser.result, list)
        True
        >>> parser.new_value_pattern.pattern
        '^counts\\['
        >>> parser = Parser(weighted=True).detect_format('counts[] = Herp, 1')
        >>> isinstance(parser.result, dict)
        True
        """
        keys_string, _ = self.cleave(line)
        varname, keys = self.parse_keys(keys_string)

        # Create a regex from the varname
        self.new_value_pattern = re.compile('^' + re.escape(varname) + '\[')

        if not self.weighted and keys[0] == '':
            # It's a simple list.
            self._container = []
        else:
            # Create a dictionary capable of autovivification.
            self._container = vivify()

        return self

    @staticmethod
    def cleave(line):
        left, right = line.split('=', 1)
        assert left[-1] == ' ' and right[0] == ' '
        return left[:-1], right[1:]

    def parse(self, iterator):
        for line in iterator:
            self.ingest(line)
        assert self._container is not None
