from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='financialdata',
    version='0.0.1',
    description='financial mining',
    long_description=long_description,
    packages=['financialdata'],

)

