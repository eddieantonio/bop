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

"""
Lose collection of utilities.
"""

from collections import defaultdict


def dedefaultdictize(d):
    """
    Converts a defaultdict into a standard Python dict, recusively.

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


def vivify():
    """
    Create a dictionary that is capable of autovivification. That is,
    accessing members that don't exist causes new dictionaries to be created.
    """
    return defaultdict(vivify)
