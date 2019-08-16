# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='concorde',
    version='0.1',
    description='Slack->Riot.im account sync',
    author='Thomas Lant',
    author_email='lampholder@gmail.com',
    url='https://github.com/lampholder/concorde',
    packages=find_packages(exclude=('tests', 'docs'))
)
