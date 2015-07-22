Posterized Image Detection
==========================

In posterized image detection first loads given image as gray scale image.
Then histogram is calculated. From the histogram average derivate and amount
of local max points. These values were then used to with the svm to calculate
final prediction. Initial idea that the average of derivate and number of
local maximums differ in posterized and non posterized images came from this
article http://www.cambridgeincolour.com/tutorials/posterization.htm and
more specifically its pictures of histograms of posterized and non posterized images.

.. image:: images/posterized_histogram.png
Histogam of posterized image

.. image:: images/non_posterized_histogram.png
HIstogram of non posterized image
