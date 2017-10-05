"""
decu
----

Decu is a Experimental Computation Utility.

"""

from setuptools import setup, find_packages


def get_requirements(suffix=''):
    with open('requirements{}.txt'.format(suffix)) as file:
        result = file.read().splitlines()
    return result

setup(
    name='decu',
    version='0.0.1',
    url='https://github.com/leotrs/decu',
    author='Leo Torres',
    author_email='leo@leotrs.com',
    description='Decu is a Experimental Computation Utility',
    long_description='',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any'
)
