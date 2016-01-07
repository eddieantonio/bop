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
parses results from Boa's less than helpful text output
"""

import re
from collections import defaultdict

__all__ = ['parse']

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
        self.result = None

    def add_result(self, *args):
        """
        >>> p = Parser()
        >>> p.result = []
        >>> p.add_result('', 'bar').result
        ['bar']
        >>> p.add_result('', 'baz').result
        ['bar', 'baz']

        >>> p = Parser(weighted=True)
        >>> p.result = {}
        >>> p.add_result('foo', '12').result
        {'foo': '12'}

        >>> p = Parser().detect_format('foo[bar][baz] = quux')
        >>> p.add_result('bar', 'baz', 'quux').result['bar']['baz']
        'quux'
        """
        assert len(args) >= 2
        keys, value = args[:-1], args[-1]

        if isinstance(self.result, list):
            self.result.append(value)
            return self

        current_dict = self.result
        for key in keys[:-1]:
            current_dict = current_dict[key]
        current_dict[keys[-1]] = value

        return self

    def parse_weight(self, string):
        """
        >>> Parser().parse_weight('GNU General Public License version 2.0 (GPLv2), 78')
        ('GNU General Public License version 2.0 (GPLv2)', '78')
        """
        assert not string.endswith('\n')
        match = WEIGHT_PATTERN.search(string)
        assert match
        return match.group(1, 2)

    def parse_line(self, raw_line):
        """
        >>> Parser().parse_line('foo[] = bar').result
        ['bar']
        >>> Parser(weighted=True).parse_line('foo[] = bar, 2').result['bar']
        '2'
        """
        line = raw_line.rstrip('\n')
        if not self.result:
            self.detect_format(line)

        keys_string, value = self.cleave(line)
        keys = self.parse_keys(keys_string)
        assert len(keys) > 0

        # Remove the "dummy" empty key for lists and weighted results.
        if isinstance(self.result, dict) and keys[-1] == '':
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
        >>> Parser().result is None
        True
        >>> isinstance(Parser().detect_format('counts[] = Herp').result, list)
        True
        >>> isinstance(Parser(weighted=True).detect_format('counts[] = Herp, 1').result, dict)
        True
        """
        keys_string, _ = self.cleave(line)
        keys = self.parse_keys(keys_string)

        if not self.weighted and keys[0] == '':
            # It's a simple list.
            self.result = []
        else:
            # Create a dictionary capable of autovivification.
            vivify = lambda: defaultdict(vivify)
            self.result = vivify()

        return self

    def cleave(self, line):
        """
        >>> Parser().cleave('licenses[] = GNU General Public License version 2.0 (GPLv2)')
        ('licenses[]', 'GNU General Public License version 2.0 (GPLv2)')
        """
        left, right = line.split('=')
        assert left[-1] == ' ' and right[0] == ' '
        return left[:-1], right[1:]

    def parse(self, iterator):
        for line in iterator:
            self.parse_line(line)
        assert self.result is not None


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
    Given an iterator that yields lines (like a file object), returns the
    parsed results. The results may be returned as a list if there are no
    discernible string keys; results are returned as a (possibly nested)
    dictionary otherwise.

    If ``weighted`` is True, indicates that the values are affixed with a
    comma-separate weight, like so:

        licenses[] = GNU General Public License version 2.0 (GPLv2), 78

    You must explicitly set ``weighted=True`` to parse this kind of data.
    Weighted data is always returned as a dictionary, with the "identifier" as
    the keys, and the weight as the values.

    >>> parse(["licenses[] = GNU General Public License version 2.0 (GPLv2)\n"])
    ['GNU General Public License version 2.0 (GPLv2)']
    >>> parse(["counts[] = GNU General Public License version 2.0 (GPLv2), 78\n"], True)
    {'GNU General Public License version 2.0 (GPLv2)': '78'}
    >>> parse(["Varargs[http://sourceforge.net/projects/baggielayout][/baggieLayout/trunk/src/org/peterMaloney/swing/baggieLayout/XmlTable.java][1161048214105000] = 1\n"])
    {'http://sourceforge.net/projects/baggielayout': {'/baggieLayout/trunk/src/org/peterMaloney/swing/baggieLayout/XmlTable.java': {'1161048214105000': '1'}}}
    """
    parser = Parser(weighted)
    parser.parse(string_iter)
    return dedefaultdictize(parser.result)

if __name__ == '__main__':
    import sys
    import json

    # Copy the argument vector; we'll modify the list below.
    args = sys.argv[:]

    if len(args) < 2:
        sys.stderr.write("Usage:   boa_parser [--weighted] output.txt\n")

    weighted = False
    if '--weighted' in args:
        weighted = True
        args.remove('--weighted')

    _, filename = args

    with open(filename) as f:
        results = parse(f, weighted)

    sys.stdout.write(json.dumps(results, indent=4, separators=(', ', ': ')))
    sys.stdout.write('\n')
