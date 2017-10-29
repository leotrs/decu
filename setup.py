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
    version='v0.0.2-rc2',
    url='https://github.com/leotrs/decu',
    download_url='https://github.com/leotrs/decu/archive/v0.0.2-rc2.tar.gz',
    author='Leo Torres',
    author_email='leo@leotrs.com',
    description='Decu is a Experimental Computation Utility',
    long_description='',
    license='MIT',
    packages=find_packages(),
    entry_points={'console_scripts': ['decu=decu.__main__:main']},
    install_requires=get_requirements(),
    zip_safe=False,
    data_files=[('decu/', ['decu/decu.cfg'])],
    include_package_data=True,
    platforms='any'
)
