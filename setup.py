from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ovhcloud',

    use_scm_version=True,
    setup_requires=['setuptools_scm'],

    description='A command-line tool for OVH API',
    long_description=long_description,

    url='https://github.com/kartoch/ovhcloud',

    author='Julien Cartigny',
    author_email='kartoch@gmail.com',

    license='GPL3',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
    ],

    keywords='cloud',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['ovh'],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    package_data={},
    data_files=[],

    entry_points={
        'console_scripts': [
            'ovhcloud=client:main',
        ],
    },
)
