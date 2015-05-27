.. _testing:


Testing of filters
******************

For testing accuracy testing was used to measure how good each filter performs.
For accuracy testing there is a module accurancy_test which provides functionality
for running the test for given data set and also to save the results. It records
accuracy of algorithm for all samples and also accuracy for each sample category
separately.

Accuracy test results of the filters
====================================

Blur detection
--------------
Here are listed accuracy test results for parts of the blur detection part of
the library.

**whole_blur module's is_blurred -function**

* For all samples correct predictions:        69,53 %
* For blurred images correct predictions: 61,22 %
* For non blurred images correct predictions:     96,67 %


Testing library code documentation
==================================

.. automodule:: accurancy_test_lib
  :members:
