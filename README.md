Boa Results Parser
==================

Parses results from [Boa][] in Python! 👍

**Note**: is not a Boa client! (I would have come up with a terrible
pun for that).

Usage
=====

Copy `boa_parser.py` into your project (what's pypi, pip, and virtualenv
lol), the use like so:

~~~ python
>>> import boa_parser
>>> with open('results.txt') as f:
>>>   results = boa_parser.parse(f)
>>> len(results)
~~~

License
=======

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
