#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

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

from .. import Parser, parse, parseiter, __version__

# Test inputs
GNU_LINE = 'licenses[] = GNU General Public License version 2.0 (GPLv2)\n'
GNU_LINE_WITH_WEIGHT = ('counts[] = GNU General Public License version 2.0 '
                        '(GPLv2), 78\n')
KEY_AND_VALUE_LINE = 'file[owner/repo] = /Makefile\n'
GNU_VALUE_WITH_WEIGHT = 'GNU General Public License version 2.0 (GPLv2), 78'
LINE_WITH_NESTED_VALUE = ('Varargs[http://sourceforge.net/projects/baggielayout]'
                          '[/baggieLayout/trunk/src/org/peterMaloney/swing/baggieLayout/XmlTable.java]'
                          '[1161048214105000] = 1\n')
LINE_WITH_SINGLE_LINE_VALUE = 'Commits[eddiantonio/bop][sha1] = herp\n'
LINE_WITH_MULTILINE_VALUE = ('Commits[eddieantonio/bop][sha2] = I herped\n\n'
                             'I derped\n\n'
                             'I conquered\n')
INPUT_WITH_MULTILINE_VALUES = """\
some_var[] = single line value
some_var[] = multi
line


value
some_var[] = last value
"""


def yield_lines(string):
    "Test helper. Yeilds one line at a time from a string."
    for line in string.split('\n'):
        yield line + '\n'


def test_add_result():
    # Adds a simple results.
    p = Parser()
    p._container = []
    assert ['bar'] == p.add_result('', 'bar').result
    assert ['bar', 'baz'] == p.add_result('', 'baz').result

    # Adds weighted results.
    p = Parser(weighted=True)
    p._container = {}
    assert {'foo': '12'} == p.add_result('foo', '12').result


def test_add_results_after_detect_format():
    p = Parser().detect_format('foo[bar][baz] = quux')
    result = p.add_result('bar', 'baz', 'quux').result
    assert {'bar': {'baz': 'quux'}} == result


def test_parse_weight():
    result = Parser().parse_weight(GNU_VALUE_WITH_WEIGHT)
    assert result == ('GNU General Public License version 2.0 (GPLv2)', '78')


def test_parse_line():
    # Test parsing a single weighted line
    result = Parser(weighted=True).parse_line('foo[] = bar, 2').result
    assert {'bar': '2'}


def test_parse_multiline_values():
    parser = Parser()
    for line in yield_lines(LINE_WITH_MULTILINE_VALUE):
        parser.ingest(line)
    expected = {
        'eddieantonio/bop': {'sha2': 'I herped\n\nI derped\n\nI conquered'}
    }
    assert expected == parser.result

    parser = Parser()
    for line in yield_lines(LINE_WITH_MULTILINE_VALUE):
        parser.ingest(line)
    parser.ingest(LINE_WITH_SINGLE_LINE_VALUE)
    expected = {
        'eddieantonio/bop': {
            'sha1': 'I herped\n\nI derped\n\nI conquered',
            'sha2': 'herp',
        }
    }


def test_cleave():
    result = Parser.cleave(GNU_LINE.rstrip())
    expected = 'licenses[]', 'GNU General Public License version 2.0 (GPLv2)'
    assert expected == result

    result = Parser.cleave(GNU_LINE_WITH_WEIGHT.rstrip())
    expected = 'counts[]', 'GNU General Public License version 2.0 (GPLv2), 78'
    assert expected == result


def test_parse():
    result = parse([GNU_LINE])
    assert ['GNU General Public License version 2.0 (GPLv2)'] == result

    result = parse([GNU_LINE_WITH_WEIGHT], weighted=True)
    assert {'GNU General Public License version 2.0 (GPLv2)': '78'} == result

    result = parse([LINE_WITH_NESTED_VALUE])
    expected = {
        'http://sourceforge.net/projects/baggielayout': {
            '/baggieLayout/trunk/src/org/peterMaloney/swing/baggieLayout/XmlTable.java': {
                '1161048214105000': '1'
            }
        }
    }
    assert expected == result


def test_parse_with_multiline_values():
    actual = parse(yield_lines(INPUT_WITH_MULTILINE_VALUES))
    expected = ['single line value', 'multi\n\nline\n\nvalue', 'last value']
    assert expected == actual


def test_parse_options():
    pass


def test_parseiter_simple():
    iterator = iter(parseiter(yield_lines(GNU_LINE)))
    iterations = 0
    for result in iterator:
        iterations += 1

        assert isinstance(result, tuple)
        assert 3 == len(result)

        # Access elements by name
        assert result.keys is None
        assert result.value == 'GNU General Public License version 2.0 (GPLv2)'
        assert result.weight is None

    assert 1 == iterations

def test_parseiter_with_keys():
    lines = yield_lines(KEY_AND_VALUE_LINE)
    iterator = iter(parseiter(lines, weight=int))
    iterations = 0
    for result in iterator:
        iterations += 1

        assert isinstance(result, tuple)
        assert 3 == len(result)

        # Access elements by name
        assert result.key == 'owner/repo'
        assert result.keys == ('owner/repo',)
        assert result.value == '/Makefile'
        assert result.weight is None

    assert 1 == iterations
