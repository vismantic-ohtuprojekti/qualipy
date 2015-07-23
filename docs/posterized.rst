Posterized image detection
==========================

Usage
-----

Class to pass to the process function: Posterized

How it works
------------

The posterized image detection first loads the given image as a grayscale image and calculates a histogram of its intensities. From this histogram the average derivative and the amount of local maxima are calculated. These values are fed to a support vector machine to calculate the final prediction. The initial idea that the average derivative and the number of local maxima differ in posterized and non-posterized images comes from `this article <http://www.cambridgeincolour.com/tutorials/posterization.htm>`_ and more specifically its pictures of histograms of both posterized and non-posterized images.

Histogram of a posterized image

.. image:: images/posterized_histogram.png

Histogram of a non-posterized image

.. image:: images/non_posterized_histogram.png
