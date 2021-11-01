#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='deprecat',
    version='1.0.0',
    url='https://github.com/mjhajharia/deprecat',
    download_url='https://github.com/mjhajharia/deprecat/archive/refs/tags/v1.0.0.tar.gz',
    license='MIT',
    author='Meenal Jhajharia',  
    author_email='meenal@mjhajharia.com',
    description='Python @deprecat decorator to deprecate old python classes, functions or methods.',
    long_description=__doc__,
    long_description_content_type="text/x-rst",
    keywords='deprecate,deprecated,deprecation,warning,warn,decorator',
    packages=['deprecat'],
    install_requires=['wrapt < 2, >= 1.10'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    extras_require={
        'dev': [
            'tox',
            'PyTest             ; python_version >= "3.6"',
            'PyTest < 5         ; python_version < "3.6"',
            'PyTest-Cov         ; python_version >= "3.6"',
            'PyTest-Cov < 2.6   ; python_version < "3.6"',
            'bump2version < 1',
            'sphinx < 2',
            # Python 2.7 EOL:
            'importlib-metadata < 3       ; python_version < "3"',
            'importlib-resources < 4      ; python_version < "3"',
            'configparser < 5             ; python_version < "3"',
            'sphinxcontrib-websupport < 2 ; python_version < "3"',
            'zipp < 2                     ; python_version < "3"',
        ]
    },
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
)
