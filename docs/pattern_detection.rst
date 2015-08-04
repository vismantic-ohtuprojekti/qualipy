Pattern detection
=================

Usage
-----

The filter can be used by itself or in combination with the *imgfilter.process* function by adding a **Pattern** class instance to the list of filters to be used.

.. currentmodule:: imgfilter.filters.pattern
.. autoclass:: Pattern
   :members:

   .. automethod:: __init__

How it works
------------
The image is first turned into grayscale, after which discrete fast fourier transformation is applied to construct the magnitude spectrum of the image. Then frequencies which have intermediate or low intensities are removed from the magnitude spectrum and all frequencies with high intensity are intensified to the max value. After this the distance from the center for each high intensity frequency is calculated. From this set of distances anomalies are removed by using the `local outlier factor method <http://en.wikipedia.org/wiki/Local_outlier_factor>`_.

The max from the set of distances is taken. This max distance is then used as a radius for a circle, and all points outside this circle in the magnitude spectrum are excluded and the density of high frequencies is calculated. This density is used to estimate how pattern-like the image is. Pattern-like images usually exhibit smaller density non-pattern-like images. The inspiration to this method came from `here <http://cs.stackexchange.com/questions/10545/image-pattern-detection-finding-similarities-in-same-image>`_ and also by looking at magnitude spectrums of both pattern- and non-pattern-like images.

.. image:: images/pattern.png
   :width: 325px
.. image:: images/non_pattern.png
   :width: 325px
