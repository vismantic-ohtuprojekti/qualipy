.. _accuracy:

Accuracy test results
*********************
This section has listed accuracy test results for filters which have been accuracy tested.
Images that have been used for accuracy testing are mainly from Flickr and Google.
If some other images have been used it is mentioned separately.

Trained SVM's which were used in these accuracy tests are provided with the project as default
SVM for each filter that uses SVM. For each accuracy test threshold of 0.5 was used if not
mentioned otherwise.

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
* Correct predictions for pattern images: 67,08 %
* Correct predictions for non pattern images: 72,73 %

Over-exposure detection
-----------------------
300 images from flickr were downloaded and labeled as either over-exposured or normal. With a threshold value of 0.5 the following results were achieved:

* Correct predictions for all samples:  87.00 %
* Correct predictions for over-exposed images: 86.00 %
* Correct predictions for normal images: 88.00 %

Posterized detection
--------------------
For 140 images downloaded from both google and flickr

* Correct predictions for all samples:  85.10 %
* Correct predictions for posterized images: 88.60 %
* Correct predictions for normal images: 81.70 %

Cross processed detection
-------------------------
For 140 images downloaded from both google and flickr

* Correct predictions for all samples:  73.60 %
* Correct predictions for cross processed images: 60.00 %
* Correct predictions for normal images: 87.10 %
