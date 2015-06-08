.. _testing:


Training classifiers
********************

Some filters work by training machine learning methods to classify
images into wanted categories. The library comes with the filters
already trained, but training scripts can be found in the folder scripts/train in the project's root directory.

Trainers
========

Blur detection
--------------
The filter can be trained using the train_svm.py script located in scripts/train. The script takes as command-line arguments the name of the filter to train and the paths to the blurred and undistorted images, i.e. for whole blur::

    python train_svm.py --whole_blur /path/to/blurred /path/to/unblurred

The classifier used in the project was trained using the `CERTH Image Blur Dataset <http://mklab.iti.gr/project/imageblur>`_.

Background blur detection
-------------------------
Similarly, background blur detection can be trained using::

    python train_svm.py --blurred_context /path/to/blurred /path/to/unblurred

Information about the training set used in the project can be found in the part of the documentation describing the filter.
