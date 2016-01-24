#!/usr/bin/env python
# coding: UTF-8

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

from collections import namedtuple

from .result import Result


class Schema(namedtuple('Schema', 'keys value weight')):
    """
    Turns parsed Boa lines into results.
    """

    def create_result(self, str_keys, str_value, str_weight=None):
        """
        >>> s = Schema(keys=(str, str), value=str, weight=None)
        >>> s.create_result(('foo', 'bar'), 'baz')
        Result(keys=('foo', 'bar'), value='baz', weight=None)
        >>> s = Schema(keys=(), value=str, weight=int)
        >>> s.create_result((), 'foo', '42')
        Result(keys=(), value='foo', weight=42)
        >>> s = Schema(keys=(int,), value=int, weight=float)
        >>> s.create_result(('42',), '1337', '32')
        Result(keys=(42,), value=1337, weight=32.0)
        """

        keys = tuple(fn(obj) for fn, obj in zip(self.keys, str_keys))
        value = self.value(str_value)
        weight = self.weight(str_weight) if str_weight is not None else None
        return Result(keys, value, weight)

    @classmethod
    def infer(cls, line, keys=None, value=None, weight=None):
        """
        Creates a new schema from the given line, and previous known values.

        >>> s = Schema.infer('file[foo/bar][baz] = value, 1')
        >>> s.keys == (str, str)
        True
        >>> s.value is str
        True
        >>> s.weight is int
        True
        """
        return Schema(keys=(str, str), value=str, weight=int)
