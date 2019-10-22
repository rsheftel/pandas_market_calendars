"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/rsheftel/pandas_market_calendars
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pandas_market_calendars',
    version='1.1',

    description='Market and exchange trading calendars for pandas',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/rsheftel/pandas_market_calendars',

    # Author details
    author='Ryan Sheftel',
    author_email='rsheftel@alumni.upenn.edu',

    # Choose your license
    license='MIT',

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

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # What does your project relate to?
    keywords='trading exchanges markets OTC datetime holiday business days',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['docs', 'examples', 'tests']),

    install_requires=['pandas>=0.18', 'pytz']
)
