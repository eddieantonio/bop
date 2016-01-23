*****************
Boa Output Parser
*****************

|pypi| |license| |docs| |travis_ci|

Parses output from Boa_ in Python! :thumbsup:

**Note**: This is **not** a Boa client! (I would have come up with
a egregious snake pun had I made that).

.. _Boa: http://boa.cs.iastate.edu/

Install
-------

Install using pip:

.. code-block:: bash

    $ pip install bop


Example
-------

Using the data `viewable here`__:

.. code-block:: python

    >>> import bop
    >>> with open('boa-job-output.txt') as f:
    ...     results = bop.parse(f, weighted=True)
    ...
    >>> results
    {'c#': '145', 'python': '127', 'php': '358', 'c': ...}

__ http://boa.cs.iastate.edu/boa/?q=boa/job/22722

License
-------

Copyright 2016 Eddie Antonio Santos

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

|  <http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


.. |pypi| image:: https://img.shields.io/pypi/v/bop.svg?style=flat-square
    :target: https://pypi.python.org/pypi/bop
    :alt: Latest stable version number on Pypi

.. |docs| image:: https://img.shields.io/badge/docs-stable-blue.svg?style=flat-square
    :target: http://b-bop.readthedocs.org/en/stable/
    :alt: Read the docs

.. |license| image:: https://img.shields.io/pypi/l/bop.svg?style=flat-square
    :target: http://www.apache.org/licenses/LICENSE-2.0
    :alt: Apache Licensed

.. |travis_ci| image:: https://img.shields.io/travis/eddieantonio/bop/master.svg?style=flat-square
    :target: http://travis-ci.org/eddieantonio/bop
    :alt: Build status of the master branch on Mac/Linux
