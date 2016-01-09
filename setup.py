from setuptools import setup
from bop import __version__ as bop_version, __doc__ as bop_description

setup(name='bop',
      version=bop_version,
      description=bop_description,
      url='http://github.com/eddieantonio/bop',
      author='Eddie Antonio Santos',
      author_email='easantos@ualberta.ca',
      license='Apache',
      packages=['bop'])
