from setuptools import setup, find_packages

setup(
    name='imgfilter',
    version='0.0.1',
    description='Image filtering suite for Vismantic',
    url='https://github.com/vismantic-ohtuprojekti/image-filtering-suite',
    author='Vismantic software engineering lab',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='image processing filtering',

    packages=find_packages(exclude=['docs', 'tests*']),
)
