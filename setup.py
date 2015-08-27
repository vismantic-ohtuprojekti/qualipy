from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst')) as f:
    long_description = f.read()

setup(
    name='QualiPy',
    version='1.0.0',
    description='Image filtering suite for Vismantic',
    long_description=long_description,

    url='https://github.com/vismantic-ohtuprojekti/image-filtering-suite',
    author='Vismantic software engineering lab',
    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='image quality processing filtering photos photography',

    packages=find_packages(exclude=['docs', 'tests*']),
    package_data={'qualipy': ['data/svm/*', 'data/object_extraction/*']},

    install_requires=[i.strip() for i in
                      open("requirements.txt").readlines()],
)
