#!/usr/bin/env python

from distutils.core import setup


py_modules = ['mytables']

setup(
    name="eztap",
    version='0.1.0a',
    author="Morgan Fouesneau",
    author_email="mfouesn@uw.edu",
    py_modules=py_modules,
    description="High-level package providing a flexible data file server.",
    long_description=open("README.md").read(),
    classifiers=[
        "Development Status :: 0 - Beta",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
