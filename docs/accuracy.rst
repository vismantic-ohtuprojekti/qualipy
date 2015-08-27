.. _accuracy:

Accuracy test results
*********************

This section lists accuracy test results for filters which have been tested for accuracy.
Images that have been used for testing are mainly collected from Flickr and
Google Images search results. If some other images have been used, it is mentioned separately.

Note that these are only meant to give a rough guideline of each filter's performance, as
they only provide a measurement for one test set with one threshold applied. For more
comprehensive results, see each filter's own documentation.

Trained SVMs which were used in these accuracy tests are provided with the project as default
SVM models for each filter that needs them. For each accuracy test, a threshold of 0.5 was used
if not otherwise mentioned.

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

Frame detection
---------------
For 400 images from Flickr there were no undetected all-around-framed images:

* Correct predictions for all samples: 99%
* Correct predictions for framed images: 100%
* Correct predictions for normal images: 98%

Highlights detection
--------------------
For 100 normal images and 70 highlighted images downloaded from Flickr:

* Correct predictions for all samples: 87%
* Correct predictions for highlighted samples: 81%
* Correct predictions for normal images: 93%

Pattern detection
-----------------
For 100 pattern images and 120 non pattern images which were downloaded from Flickr:

* Correct predictions for all samples: 70,37 %
* Correct predictions for pattern images: 67,08 %
* Correct predictions for non pattern images: 72,73 %

Exposure detection
-----------------------
300 images from flickr were downloaded and used to form three groups: original untouched images, images modified to be under-exposed and images modified to be over-exposed. When the modified groups were put in the same folder and compared to the original photos, we got the following results:

* Correct predictions for all samples:  87.00 %
* Correct predictions for over-exposed/under-exposed images: 85.00 %
* Correct predictions for normal images: 90.00 %

Posterized detection
--------------------
For 140 images downloaded from both google and Flickr

* Correct predictions for all samples:  85.10 %
* Correct predictions for posterized images: 88.60 %
* Correct predictions for normal images: 81.70 %

Cross processed detection
-------------------------
For 140 images downloaded from both google and Flickr. In this threshold of 0.4 was used.

* Correct predictions for all samples:  73.60 %
* Correct predictions for cross processed images: 60.00 %
* Correct predictions for normal images: 87.10 %

HDR detection
-------------

For training the HDR detection, 225 normal and 225 HDR images were downloaded from Flickr and Google Images search and labeled by hand. From these sets, 50 blurred and 50 undistorted images were randomly moved before training from the training set to a separate evaluation set. The filter's performance for this evaluation set is as follows:

* Correct predictions for all samples:  86.66 %
* Correct predictions for HDR images: 88.88 %
* Correct predictions for normal images: 84.44 %
