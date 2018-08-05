#!/usr/bin/python3
#
# Simple setup.py to install piplayer module + the command line shell
# script to run it.

from os import path
from setuptools import setup

setup(
    name="piplayer",
    version="1.0.0",
    author="sconley",
    author_email="cheetah@tanabi.org",
    description="A simple MP3 Player for Raspberry Pi's",
    license="Public Domain",
    keywords="raspberry pi music player tornado backend",
    url="https://github.com/tanabi/piplayer",
    packages=[
        'piplayer',
    ],
    long_description=open(path.join(path.dirname(__file__), 'README.md')).read(),
    scripts=[
        'scripts/piplayer',
    ],
    install_requires=[
        'mutagen',
        'tornado'
    ],
    zip_safe=False
)
