from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ovhcloud',

    use_scm_version=True,
    setup_requires=['setuptools_scm', 'pytest-runner'],

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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='cloud ovh',

    packages=find_packages(exclude=['tests']),

    package_data={'ovhcloud': ['api.yaml']},

    install_requires=['ovh'],

    tests_require=['pytest'],

    entry_points={
        'console_scripts': [
            'ovhcloud=client:main',
        ],
    },
)
