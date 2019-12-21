from setuptools import setup

import py2exe


setup(
    name='NetworkTables Server GUI',
    version='0.1',
    description='Simple way to interact and debug NetworkTables',
    author='Nick',
    install_requires=['PySimpleGUI', 'pynetworktables'],
    console=['main.py']
)
