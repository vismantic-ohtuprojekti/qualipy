Blurred context
===============

Usage
-----

The filter can be used in combination with the imgfilter.process function by adding a **BlurredContext** class instance to the list of filters to be used.

Parameters
----------

.. currentmodule:: imgfilter.filters.blurred_context
.. autoclass:: BlurredContext

The **threshold** parameter is used to define the point where higher values than the threshold (default 0.5) are classified as blurred. The effect of different thresholds can be seen in the following graph, where x-axis is the threshold and y-axis is the percentage of correct predictions:

.. image:: images/thresholds_blurred_context.png
   :width: 650px

How it works
------------

The filter first constructs a so-called "blur map" from the image using the method described by Su et al in their paper *Blurred Image Region Detection and Classification* (Proceedings of the 19th ACM International Conference on Multimedia, 2011): for each pixel, its "blurry degree" is estimated using the following formula:

.. math::

    \beta = \frac{\lambda_1}{\sum_{i=1}^5 \lambda_i}

where :math:`\lambda_i` are the singular values obtained by doing a singular value decomposition on a 5px x 5px patch (larger patches can be used for slightly better results, but at cost in runtime) surrounding the pixel. Example blur map:

.. image:: images/shoe.jpg
   :width: 325px
.. image:: images/blurmap_shoe.png
   :width: 325px

This blur map is then broken into 100 partitions of equal size and the mean value of each partition is used as variable in an input vector that is fed into a support vector machine. The default support vector machine has been trained using 450 blurred and 450 undistorted images that were downloaded from Flickr and labeled by hand.

Sample "blurred context" images from the training set:

.. image:: images/blurred_context_sample1.jpg
   :width: 215px
.. image:: images/blurred_context_sample2.jpg
   :width: 215px
.. image:: images/blurred_context_sample3.jpg
   :width: 215px

Sample undistorted images from the training set:

.. image:: images/blurred_context_sample4.jpg
   :width: 215px
.. image:: images/blurred_context_sample5.jpg
   :width: 215px
.. image:: images/blurred_context_sample6.jpg
   :width: 215px
