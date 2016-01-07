Boa Results Parser
==================

[![Build Status](https://travis-ci.org/eddieantonio/boa_parser.svg?branch=master)](https://travis-ci.org/eddieantonio/boa_parser)

Parses results from [Boa][] in Python! 👍

**Note**: This is not a Boa client! (I would have come up with
a egregious snake-based pun had I made that).

Usage
-----

Copy `boa_parser.py` into your project (what's pypi, pip, and virtualenv
lol).

Example
-------

Using the data [viewable here][example-job]:

~~~ python
>>> import boa_parser
>>> with open('boa-job-output.txt') as f:
...     results = boa_parser.parse(f, weighted=True)
...
>>> results
{'c#': '145', 'python': '127', 'php': '358', 'c': ...}
~~~

License
-------

    Copyright 2016 Eddie Antonio Santos <easantos@ualberta.ca>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

[Boa]: http://boa.cs.iastate.edu/
[example-job]: http://boa.cs.iastate.edu/boa/?q=boa/job/22722
