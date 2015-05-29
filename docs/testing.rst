.. _testing:


Testing of filters
******************

Accuracy testing was used to measure how well each filter performs.
For accuracy testing there is a module accuracy_test which provides functionality
for running the test for given data set and also to save the results. It records
the accuracy of algorithm for all samples and also the accuracy for each sample category
separately.

Accuracy test results of the filters
====================================

Blur detection
--------------
Here are the accuracy test results for the whole blur detection function
when using the `CERTH Image Blur Dataset <http://mklab.iti.gr/project/imageblur>`_.

**whole_blur module's is_blurred -function**

* For all samples correct predictions:        80,30 %
* For blurred images correct predictions: 72,51 %
* For non blurred images correct predictions:     85,74 %


Testing library code documentation
==================================
