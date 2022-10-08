"""
A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
"""

from os import path

from setuptools import find_packages, setup

# version
VERSION = '4.0.2'

# requirements
REQUIRED_PYTHON = '>=3.8.0'
REQUIRED_PACKAGES = ['pandas>=1.1', 'pytz', 'python-dateutil', 'exchange_calendars>=3.3']

# Package meta-data
NAME = 'pandas_market_calendars'
DESCRIPTION = 'Market and exchange trading calendars for pandas'
SOURCE_URL = 'https://github.com/rsheftel/pandas_market_calendars'
DOCS_URL = 'https://pandas-market-calendars.readthedocs.io/en/latest/'
AUTHOR = 'Ryan Sheftel'
EMAIL = 'rsheftel@alumni.upenn.edu'
LICENSE = 'MIT'

# ----- items below do not generally change ------- #

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    # meta data
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url=SOURCE_URL,
    author=AUTHOR,
    author_email=EMAIL,
    license=LICENSE,
    project_urls={
        'Documentation': DOCS_URL,
        'Source': SOURCE_URL,
    },

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here.
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],

    # What does your project relate to?
    keywords='trading exchanges markets OTC datetime holiday business days',

    # requirements
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    python_requires=REQUIRED_PYTHON,
    install_requires=REQUIRED_PACKAGES,
    tests_require=['pytest'],
)
