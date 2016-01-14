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
bop - parses results from Boa's less than helpful text output
"""

import re
from collections import defaultdict

__all__ = ['parse']
__version__ = '0.1.0'

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
        self.line = ''
        self.value = ''
        self._container = None

    @property
    def result(self):
        if self._container is None:
            raise RuntimeError('Container type not yet determined '
                               '(parse at least one line of input)')
        return self._container

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

    def parse_weight(self, string):
        assert not string.endswith('\n')
        match = WEIGHT_PATTERN.search(string)
        assert match
        return match.group(1, 2)

    def parse_line(self, raw_line):
        """
        >>> Parser().parse_line('foo[] = bar').result
        ['bar']
        """
        line = raw_line.rstrip('\n')
        if not self._container:
            self.detect_format(line)

        keys_string, value = self.cleave(line)
        keys = self.parse_keys(keys_string)
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

    def parse_keys(self, keys_string):
        """
        >>> Parser().parse_keys('counts[foo][bar]')
        ['foo', 'bar']
        >>> Parser().parse_keys('counts[]')
        ['']
        """
        parsed = KEY_PATTERN.split(keys_string)
        assert len(parsed) > 1
        # Results are in every SECOND item.
        return parsed[1::2]

    def detect_format(self, line):
        r"""
        >>> Parser().result
        Traceback (most recent call last):
            ...
        RuntimeError: Container type not yet determined ...
        >>> isinstance(Parser().detect_format('counts[] = Herp').result, list)
        True
        >>> parser = Parser(weighted=True).detect_format('counts[] = Herp, 1')
        >>> isinstance(parser.result, dict)
        True
        """
        keys_string, _ = self.cleave(line)
        keys = self.parse_keys(keys_string)

        if not self.weighted and keys[0] == '':
            # It's a simple list.
            self._container = []
        else:
            # Create a dictionary capable of autovivification.
            vivify = lambda: defaultdict(vivify)
            self._container = vivify()

        return self

    @staticmethod
    def cleave(line):
        left, right = line.split('=')
        assert left[-1] == ' ' and right[0] == ' '
        return left[:-1], right[1:]

    def parse(self, iterator):
        for line in iterator:
            self.parse_line(line)
        assert self._container is not None


def dedefaultdictize(d):
    """
    >>> vivify = lambda: defaultdict(vivify)
    >>> d = vivify()
    >>> d['foo'][0]['bar'] = 'baz'
    >>> d['foo'][1] = 'quux'
    >>> dedefaultdictize(d)
    {'foo': {0: {'bar': 'baz'}, 1: 'quux'}}
    """
    if not isinstance(d, dict):
        return d
    return {k: dedefaultdictize(v) for k, v in d.items()}


def parse(string_iter, weighted=False):
    r"""
    Given an iterator that yields strings (like a file object), returns the
    parsed results. The results may be returned as a list if there are no
    discernible string keys; results are returned as a (possibly nested)
    dictionary otherwise.

    If ``weighted`` is ``True``, indicates that the values are affixed with a
    comma-separate weight, like so::

        licenses[] = GNU General Public License version 2.0 (GPLv2), 78

    You must explicitly set ``weighted=True`` to parse this kind of data.
    Weighted data is always returned as a dictionary, with the "identifier" as
    the keys, and the weight as the values.

    :param string_iter: A string or an iterator that yields strings, such as
                        a :any:`file` object.
    :param bool weighted: Whether the output consists of weights.
    :return: parsed Boa output
    :rtype: :py:class:`dict` or :py:class:`list`

    """
    parser = Parser(weighted)
    parser.parse(string_iter)
    return dedefaultdictize(parser.result)


def main():
    import sys
    import json

    # Copy the argument vector; we'll modify the list below.
    args = sys.argv[:]

    if len(args) < 2:
        sys.stderr.write("Usage:   bop [--weighted] output.txt\n")
        sys.exit(-1)

    weighted = False
    if '--weighted' in args:
        weighted = True
        args.remove('--weighted')

    _, filename = args

    with open(filename) as f:
        results = parse(f, weighted)

    sys.stdout.write(json.dumps(results, indent=4, separators=(', ', ': ')))
    sys.stdout.write('\n')

if __name__ == '__main__':
    main()
