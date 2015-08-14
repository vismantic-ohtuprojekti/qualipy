Posterized
==========

Usage
-----

The filter can be used by itself or in combination with the *imgfilter.process* function by adding a **Posterized** class instance to the list of filters to be used.

.. currentmodule:: imgfilter.filters.posterized
.. autoclass:: Posterized
   :members:

   .. automethod:: __init__

How it works
------------

The posterized image detection first loads the given image as a grayscale image and calculates a histogram of its pixel intensities.
From this histogram the value for each local max point calculated which measures how sharp the peak is. Calculating value takes into account
how wide the peak is meaning how big distance is between local min before the local max point and after it. Second feature that
is measured is how large peak is meaning how the is average difference between value at local max and two local mins next to it.
Posterized images have naturally more sharp peaks since colors in image are lacking many different shades. There are images of both
typical posterized image and normal image. Also Roc curve of posterized detection is provided.

Histogram of a posterized image

.. image:: images/posterized_histogram.png

Histogram of a non-posterized image

.. image:: images/non_posterized_histogram.png

Histogram of non posterized image

.. image:: images/posterized_roc_curve.png

Roc curve of posterized image filter
