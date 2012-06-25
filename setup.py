#!/usr/bin/env python

from distutils.core import setup
import os
import setuplib

packages, package_data = setuplib.find_packages('feincms_oembed')

setup(name='feincms-oembed',
    version=__import__('feincms_oembed').__version__,
    description='OEmbed anything.',
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author='FEINHEIT GmbH',
    author_email='kontakt@feinheit.ch',
    url='https://github.com/feincms/feincms-oembed/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=packages,
    package_data=package_data,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
