from __future__ import print_function
from setuptools import setup, find_packages, Command
import sys
import io, os

NAME = "polarishub"
DESCRIPTION = 'A p2p file transfer program via LAN.'
URL = "https://github.com/XieGuochao/polarishub"
EMAIL = 'senyuehao@link.cuhk.edu.cn'
AUTHOR = 'Xie Guochao & Hao Senyue'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.9.0'

REQUIRED = [
    'Django>=2.1.5','MyQR==2.3.1'
]

try:
    with io.open(os.path.join(here, 'ReadMe for Python Library.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)