#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
# - Have access to the azure resource object storage
# - $ python3 setup.py sdist bdist_wheel --universal

import io
import os
import sys
import subprocess
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'cvpartnerpy'
DESCRIPTION = 'A python package for scraping cvpartner api'
URL = 'https://github.com/peakBreaker/cvpartnerpy'
EMAIL = 'andershurum@gmail.com'
AUTHOR = 'Anders L. Hurum'
REQUIRES_PYTHON = '>=3.5.0'
DEFAULT_VERSION = '0.0.0'  # Invalid version

# What packages are required for this module to be executed?
with open('requirements.txt', 'r') as f:
    REQUIRED = f.read().split('\n')

# REQUIRED = [
    # 'requests'
# ]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
about['__version__'] = os.environ.get('CVPARTNER_PY_VERSION', DEFAULT_VERSION)

print('Libarary version is set to {}'.format(about["__version__"]))


class CleanCommand(Command):
    """Support for setup.py clean"""

    description = 'Cleans build and dist'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            print('CLEAR:INFO: Removing previous builds...')
            rmtree(os.path.join(here, 'dist'))
            print('CLEAR:INFO: Successfully removed prev builds!')
        except OSError:
            pass


class PublishCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things with some formatting"""
        print('PUBLISH:STATUS: {0}'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        dist_dir = os.path.join(here, 'dist')
        self.status('Build done - ls of dist: {}'.format(os.listdir(dist_dir)))

        # If we ever want to open source the package
        self.status('Uploading the package to PyPI via Twine')
        subprocess.check_call("twine upload dist/* --verbose", shell=True)

        self.status('Success! Exiting..')
        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='All rights reserved',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
    },
    #scripts=['bin/funny-joke.sh'],
    # $ setup.py publish support.
    cmdclass={
        'clear': CleanCommand,
        'publish': PublishCommand
    },
)
