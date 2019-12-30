#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup script for Anno."""

from setuptools import find_packages, setup


# -----------------------------------------------------------------------------

description = 'Anno is a thin user interface on Markdown files for easy and ' \
              'local text editing, organization, and program composability.'

setup_args = dict(
    name='anno',
    version='0.0.2',
    license='MIT',
    author='Gregory Gundersen',
    author_email='greg@gregorygundersen.com',
    description=description,
    url='https://github.com/gwgundersen/anno',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['flask>=1.1.1', 'pypandoc>=1.4'],
    entry_points={'console_scripts': ['anno = anno.annoapp:main']},
    python_requires='>=3.6'
)


def main():
    setup(**setup_args)


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()
