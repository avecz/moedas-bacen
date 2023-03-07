from setuptools import setup, find_packages

setup(name='bacenquery',
version='0.1',
description='Functions to batch call the APIs created by the python-bcb module',
url='#',
author='Pedro Cruz',
install_requires=['python-bcb'],
author_email='datascience@abelpedro.com',
packages=find_packages(),
zip_safe=False)