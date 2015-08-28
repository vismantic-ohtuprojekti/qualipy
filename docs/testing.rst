.. _testing:

Testing the project
*******************

Running tests
=============

To run unit tests for the project, run::

    py.test

in the project's root folder. This requires the pytest package to be installed. Current test coverage can be seen `here <https://coveralls.io/github/vismantic-ohtuprojekti/qualipy>`_.

Accuracy tests are provided as scripts in tests/accuracy and can be run, for example::

    python tests/accuracy/exposure.py positives/ negatives/

What's been tested
==================

Accuracy testing was used to measure how well each filter performs for a collection of hand-picked test images. Results for these accuracy tests  are in the "Accuracy test results" section of the documentation, as well as graphs in the documentation for individual filters. See above how to run accuracy tests for your chosen filter.

To test written code for bugs and to aid refactoring, unit testing was employed. The project makes use of the pytest package for unit tests and pytest-cov for the test coverage results. These tests are also automatically run for each commit on the continuous integration server, provided by `Travis <https://travis-ci.org/vismantic-ohtuprojekti/qualipy>`_.

The unit tests for each filter test at least the filter's basic functionality, for example that the filter makes correct predictions for sample images and that setting the threshold and returning the correct type work. The unit tests also test the functions used in the implementation for each filter and that the filter raises proper exceptions when called with invalid arguments or images that don't exist.

The common utilities used by the filters are also thoroughly unit tested. Functions are tested for different sample cases as well as some corner cases. Utilities are also tested for raising proper exceptions when called with invalid arguments.

In addition to automated testing, manual testing has also been performed extensively. The project and each individual filter has been tested in use outside the library. Some functionality unsuitable for unit testing, mainly the object extraction functionality, has been tested manually instead of by automated tests.
