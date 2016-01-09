==================
Boa Output Parser
==================

.. image:: https://travis-ci.org/eddieantonio/boa_parser.svg?branch=master
    :target: https://travis-ci.org/eddieantonio/boa_parser

Parses output from Boa_ in Python! :thumbsup:

**Note**: This is **not** a Boa client! (I would have come up with
a egregious snake pun had I made that).

.. _Boa: http://boa.cs.iastate.edu/

Install
-------

Install using pip::

    pip install bop


Example
-------

Using the data `viewable here`__::

    >>> import bop
    >>> with open('boa-job-output.txt') as f:
    ...     results = bop.parse(f, weighted=True)
    ...
    >>> results
    {'c#': '145', 'python': '127', 'php': '358', 'c': ...}

__ http://boa.cs.iastate.edu/boa/?q=boa/job/22722

License
-------

| Copyright 2016 Eddie Antonio Santos <easantos@ualberta.ca>
|
| Licensed under the Apache License, Version 2.0 (the "License");
| you may not use this file except in compliance with the License.
| You may obtain a copy of the License at
|
|   <http://www.apache.org/licenses/LICENSE-2.0>
|
| Unless required by applicable law or agreed to in writing, software
| distributed under the License is distributed on an "AS IS" BASIS,
| WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
| See the License for the specific language governing permissions and
| limitations under the License.
