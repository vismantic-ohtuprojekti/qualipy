# QualiPy

[![Build](https://travis-ci.org/vismantic-ohtuprojekti/qualipy.svg)](https://travis-ci.org/vismantic-ohtuprojekti/qualipy)
[![Documentation](https://readthedocs.org/projects/image-filtering-suite/badge/?version=latest)](https://image-filtering-suite.readthedocs.org/en/latest/)
[![Coverage Status](https://coveralls.io/repos/vismantic-ohtuprojekti/qualipy/badge.svg?branch=master&service=github)](https://coveralls.io/github/vismantic-ohtuprojekti/qualipy?branch=master)
[![PyPI](https://img.shields.io/pypi/v/qualipy.svg)](https://pypi.python.org/pypi/QualiPy)

### Introduction

This is a student software engineering project of the Department of Computer Science of the University of Helsinki. The aim is to develop a set of image (photo) filtering components for Vismantic, an interactive system generating visual ideas (imagine a light bulb grows out of a tuft of green leaves). Vismantic finds photos in Flickr using keywords input by a user, and then analyzes and combines these photos in different ways. Among the image processing techniques used by Vismantic, object extraction and texture transfer techniques are relevant to this project.

QualiPy (originally The Image Filtering Suite for Vismantic) implements image filtering modules that automate the filtering of images unsuitable for use in Vismantic. The library is currently able to detect e.g. images that are blurred, overexposed, pattern-like or of unconventional size. Image processing tasks utilize the NumPy and OpenCV libraries extensively. Additional features are included, such as the ability to handle image processing tasks from JSON requests and the library is optimized to be as fast as possible with vectorized operations and Numba integration.

[Documentation](https://image-filtering-suite.readthedocs.org/en/latest/)

### Getting started
For getting started, see [installation](https://image-filtering-suite.readthedocs.org/en/latest/installation.html) and [usage examples](https://image-filtering-suite.readthedocs.org/en/latest/examples.html).

### Definition of Done
- Complete unit testing for written code
- Acceptance testing with reasonable success rate
- Sufficient documentation of implemented code
- Continuous integration with travis
- Code follows Clean Code principles
- Acceptance of customer

### Scrum Documents

[Product and Sprint backlogs](https://docs.google.com/spreadsheets/d/15ugZgpvPXJk9YW2QH9u6OZCt2mqqrmE4L-Nj0N-xv4s)

### Customer meeting agendas

[Meeting 15.5.2015](https://docs.google.com/document/d/1uu15eUaOxoAChaYHmOUHUR4sALaSXURRhLW95zWfYqA)

[Meeting 29.5.2015](https://docs.google.com/document/d/1o2An2k8WWinljYI2fv5ghrk242XUyBkfp-rzEuphrCQ/edit)

[Meeting 12.6.2015](https://docs.google.com/document/d/1ymfgk3zg91ZPvp2bmUv3yexRLuKo-2_Ir1EsCp8sxhY/edit?usp=sharing)

[Meeting 25.6.2015](https://docs.google.com/document/d/1MxCtHgHj_DaHPktn7ZqgoRC3UHQ26DoYEMzGM0-EPZs/edit?usp=sharing)

[Meeting 24.7.2015](https://docs.google.com/document/d/1HjNiVAZvT8-a8zISrfPU2WmXOAR9hpz2YmfYnZJBpKg/edit?usp=sharing)

[Meeting 07.8.2015](https://docs.google.com/document/d/1vlwAQvZowyo_An2fpclNpwQTUD3Ha2SixWiMoA_GqN0/edit?usp=sharing)

[Meeting 21.8.2015](https://docs.google.com/document/d/1D5QyFqNyk8VzXLBVeXPtDPW4IvkmkF_i0Hp0fHLC14w/edit?usp=sharing)

[Meeting 28.8.2015](https://docs.google.com/document/d/1VQ76ubbNIKodq-dcgsViwugW146T9NpUUEEYJQ9R200/edit?usp=sharing)
