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
    download_url='https://github.com/leotrs/decdu/archive/0.0.1.tar.gz',
    author='Leo Torres',
    author_email='leo@leotrs.com',
    description='Decu is a Experimental Computation Utility',
    long_description='',
    license='MIT',
    packages=find_packages(),
    entry_points={'console_scripts': ['decu=decu.__main__:main']},
    zip_safe=False,
    data_files=[('decu/', ['decu/decu.cfg'])],
    include_package_data=True,
    platforms='any'
)
