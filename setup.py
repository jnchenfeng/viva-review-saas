#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="viva-review-saas",
    version='0.0.2',
    author='feng.chen',
    author_email='feng.chen@quvideo.com',
    url='https://github.com/jnchenfeng/viva-review-saas',
    description='viva review saas sdk',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords='viva review',
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'review_saas'},
    packages=find_packages('review_saas'),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)
