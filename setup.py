# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name = 'cifero',
    version = '1.0',
    url = 'https://github.com/mypackage.git',
    author = 'Jonathan J',
    author_email = 'jonjau3Q@gmail.com',
    description = 'A personal Python GUI program for phonetic transliteration/encryption',
    license='MIT',
    packages = find_packages(),
    install_requires = ['PyQt5', 'pyperclip'],
)
