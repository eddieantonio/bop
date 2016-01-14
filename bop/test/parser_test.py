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

from .. import Parser, dedefaultdictize, parse

# Test inputs
GNU_LINE = 'licenses[] = GNU General Public License version 2.0 (GPLv2)\n'
GNU_LINE_WITH_WEIGHT = "counts[] = GNU General Public License version 2.0 (GPLv2), 78\n"
GNU_VALUE_WITH_WEIGHT = 'GNU General Public License version 2.0 (GPLv2), 78'
LINE_WITH_NESTED_VALUE = 'Varargs[http://sourceforge.net/projects/baggielayout][/baggieLayout/trunk/src/org/peterMaloney/swing/baggieLayout/XmlTable.java][1161048214105000] = 1\n'


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
    result = dedefaultdictize(p.add_result('bar', 'baz', 'quux').result)
    assert {'bar': {'baz': 'quux'}} == result


def test_parse_weight():
    result = Parser().parse_weight(GNU_VALUE_WITH_WEIGHT)
    assert result == ('GNU General Public License version 2.0 (GPLv2)', '78')


def test_parse_line():
    result = Parser(weighted=True).parse_line('foo[] = bar, 2').result
    assert {'bar': '2'}


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
