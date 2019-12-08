#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup script for Anno"""

from setuptools import setup, find_packages


# -----------------------------------------------------------------------------

NAME = 'anno'

setup_args = dict(
    name=NAME,
    version='0.1',
    license='MIT',
    description='',
    long_description='',
    author='Gregory Gundersen',
    author_email='greg@gregorygundersen.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['flask', 'pypandoc'],
    entry_points={
        'console_scripts': [
            'anno = anno.annoapp:main',
        ]
    }
)


def main():
    setup(**setup_args)


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()
