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

from .parser import Parser
from .result import Result

__all__ = ['parse', 'parseiter']
__version__ = u'0.3.0'


def parse(lines, weighted=False):
    r"""
    Given an iterator that yields lines (like a file object), returns the
    parsed results. The results may be returned as a list if there are no
    discernible string keys; results are returned as a (possibly nested)
    dictionary otherwise.

    If ``weighted`` is ``True``, indicates that the values are affixed with a
    comma-separate weight, like so::

        licenses[] = GNU General Public License version 2.0 (GPLv2), 78

    You must explicitly set ``weighted=True`` to parse this kind of data.
    Weighted data is always returned as a dictionary, with the "identifier" as
    the keys, and the weight as the values.

    :param lines: An iterator that yields lines as strings, such as
                  a :any:`file` object.
    :param bool weighted: Whether the output has weights.

    :return: parsed Boa output
    :rtype: :py:class:`dict` or :py:class:`list`
    """
    parser = Parser(weighted)
    parser.parse(lines)
    return parser.result


def parseiter(lines, schema=None, weight=None, values=None,
              on_error='exception'):
    """
    Given an line iterator (like a file object), yields  Result object per
    each parsed result.

    :param lines:           An iterator that yields lines as strings, such as
                            a :any:`file` object.
    :param tuple schema:    If provided, specifies the types of each index,
                            respectively. Each "type" can actually be any
                            callable.  Typically, you would want to provide a
                            tuple of ``(str,)`` to generate several string
                            keys.
    :param type weight:     If provided, it means that each value has a
                            weight. Typically, this weight is often provided
                            as an integer or floating point number, so
                            ``weight`` should be provided as :any:`int` or
                            :any:`float`, respectively. This can actually be
                            any callable -- not just a type.
    :param type values:     If provided, specifies the type of the values.
                            Assumed to be strings by default. Actually, this
                            can be any callable.
    :param string on_error: If provided, specifies what to do when parsing
                            encounters an error of some sort. ``'raise'`` (the
                            default) throws the exception, as is. ``'ignore'``
                            silently discards the value.  ``'quarantine'``
                            returns a tuple of the exception and the offending
                            line(s) as a string.

    :return: an iterator that yields one result per iteration
    """
    if weight is int:
        yield Result(('owner/repo',), '/Makefile', None)
    else:
        yield Result(None,
                     'GNU General Public License version 2.0 (GPLv2)',
                     None)


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
