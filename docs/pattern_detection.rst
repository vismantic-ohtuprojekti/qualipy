.. _pattern_detection

Pattern detection
=================

How it works
------------
The filter first turns image into gray scale. Then Discrete Fast Fourier transform and logaritmig
scaling are used to construct magnitude spectrum of the image. Then frequencies which have intermediate
or low intensity are removed from the magnitude spectrum and all frequencies with high intensity
are intensified to the max value. After this the distance from the center for each high intensity
frequency is calculated. From this set of distances anomalies are removed by using local outliner
factor method (http://en.wikipedia.org/wiki/Local_outlier_factor). After this max from the set of
distances is taken. This max distance is then used as a radii for a circle. after this all points
outside this circle in the magnitude spectrum are excluded and density of high frequencies is calculated.
This density is used to estimate how pattern like the image is. Pattern like images usually smaller
density when algorithm is used than non pattern like images. Inspiration to this method came from
here http://cs.stackexchange.com/questions/10545/image-pattern-detection-finding-similarities-in-same-image
and also by looking magnitude spectrums of both pattern and non pattern like images.

.. image:: images/pattern.png
   :width: 325px
.. image:: images/non_pattern.png
   :width: 325px
