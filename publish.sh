#!/usr/bin/env bash

pip install setuptools wheel twine

./setup.py clean
./setup.py sdist bdist_wheel
./setup.py publish --verbose
