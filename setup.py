#!/usr/bin/env python

import os

from setuptools import find_packages, setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="feincms-oembed",
    version=__import__("feincms_oembed").__version__,
    description="OEmbed anything.",
    long_description=read("README.rst"),
    author="FEINHEIT GmbH",
    author_email="dev@feinheit.ch",
    url="https://github.com/feincms/feincms-oembed/",
    license="BSD License",
    platforms=["OS Independent"],
    packages=find_packages(exclude=["tests"]),
    package_data={
        "": ["*.html", "*.txt"],
        "feincms_oembed": [
            "locale/*/*/*.*",
            # 'static/feincms_oembed/*.*',
            # 'static/feincms_oembed/*/*.*',
            "templates/*.*",
            "templates/*/*.*",
            "templates/*/*/*.*",
            "templates/*/*/*/*.*",
        ],
    },
    install_requires=["FeinCMS>=1.15"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
