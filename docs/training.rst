.. _testing:


Training classifiers
********************

Some filters work by training machine learning methods to classify
images into wanted categories. The library comes with the filters
already trained, but training scripts can be found in the folder
train in the project's root directory.

Trainers
========

Blur detection
--------------

The whole_blur.py training script takes as arguments the path to
the blurred images and the path to the unblurred images as command-line
arguments, for example::

    python whole_blur.py /path/to/blurred /path/to/unblurred
