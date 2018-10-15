# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name = 'cifero',
    version = '1.0',
    url = 'https://github.com/jonjau/cifero',
    author = 'Jonathan J',
    author_email = 'jonjau3Q@gmail.com',
    description = 'A personal Python GUI program for phonetic transliteration.',
    license='MIT',
    packages = find_packages(),
    install_requires = ['PyQt5', 'pyperclip'],
)
