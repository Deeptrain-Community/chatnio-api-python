#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "httpx>=0.13.3",
    "websockets>=8.1",
]

test_requirements = []

setup(
    author="Deeptrain Community",
    author_email='zmh@lightxi.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="The official Python library for the Chat Nio API ",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='chatnio',
    name='chatnio',
    packages=find_packages(include=['chatnio', 'chatnio.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Deeptrain-Community/chatnio-api-python',
    version='0.1.2',
    zip_safe=False,
)
