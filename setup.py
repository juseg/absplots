#!/usr/bin/env python
# Copyright (c) 2019, Julien Seguinot <seguinot@vaw.baug.ethz.ch>
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""Build script for absplots."""

import setuptools

with open('README.rst', 'r') as f:
    README = f.read()

setuptools.setup(
    name='absplots',
    version='0.1.0',
    author='Julien Seguinot',
    author_email='seguinot@vaw.baug.ethz.ch',
    description='Matplotlib subplots with absolute margins in mm or inches',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='http://github.com/juseg/absplots',
    license='gpl-3.0',
    install_requires=['matplotlib'],
    py_modules=['absplots'],
)
