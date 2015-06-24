Multiple salient regions
========================

Usage
-----

The filter can be used in combination with the imgfilter.process function by adding a **MultipleSalientRegions** class instance to the list of filters to be used.

How it works
------------

First, the full saliency map is extracted using the object extraction algorithm:

.. image:: images/multiple_salient_regions.jpg

Saliency map is binarised using threshold which is counted for individually for
each image. In threshold calculation weighted average of 3/4 of biggest rounded
saliency values are used. After image is binarized all solid regions.
All regions and their sizes are calculated. After this prediction is constructed
by dividing sum of all regions by the area of the largest region. This result
is then raised to the power of two. From this 1 is substracted and this is
the final prediction. This way if saliency map contains some small separate
areas whole image is not considered to have multiple saliency regions.

Example of image which contains multiple saliency regions:

Saliency map

.. image:: images/saliency_map_for_multiple_saliency_regions.png

Binarized saliency map

.. image:: images/binarized_saliency_map_for_multiple_saliency_regions.png

For this image limit which was used for binarization was 92.65 and
given prediction was 1.0


Example of image which doesn't contain multiple saliency regions

Saliency map

.. image:: images/saliency_map_of_one_saliency_region.png

Binarized saliency map

.. image:: images/binarized_saliency_map_of_non_multiple_saliency_regions.png

For this image limit which was used for binarization was 113.25 and
given predection was 0.31

When using multiple saliency regions filter threshold of 0.5 was tested to be the
best one.
