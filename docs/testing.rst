.. _testing:


Testing of filters
******************

Accuracy testing was used to measure how well each filter performs.  For accuracy testing, there is a module accuracy_test which provides functionality for running the test for a given datase. It records the accuracy of the algorithm for all samples and as well as the accuracy for each sample category separately.

Accuracy test results of the filters
====================================

Blur detection
--------------
Accuracy test results for the whole blur filter using the `CERTH Image Blur Dataset <http://mklab.iti.gr/project/imageblur>`_:

* Correct preditions for all samples: 80,30 %
* Correct predictions for blurred images: 72,51 %
* Correct predictions for undistorted images: 85,74 %

Blurred context detection
-------------------------
For training the blurred context detection, 525 blurred and 525 undistorted images were downloaded from Flickr and labeled by hand. From these sets, 75 blurred and 75 undistorted images were randomly moved before training from the training set to a separate evaluation set. The filter's performance for this evaluation set is as follows:

* Correct predictions for all samples: 90,00 %
* Correct predictions for blurred images: 92,00 %
* Correct predictions for undistorted images: 88,00 %

Pattern detection
-----------------
For 100 pattern images and 120 non pattern images which were downloaded from Flickr:
* Correct predictions for all samples: 70,37 %
* Correct predictions for pattern images: 67.08 %
* Correct predictions for non pattern images: 72,73 %


Testing library code documentation
==================================
