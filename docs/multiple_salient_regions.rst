Multiple salient regions
========================

Usage
-----

The filter can be used in combination with the imgfilter.process function by adding a **MultipleSalientRegions** class instance to the list of filters to be used.

How it works
------------

First, the full saliency map is extracted using the object extraction algorithm:

.. image:: images/multiple_salient_regions.jpg

This saliency map is binarized by marking all pixels with intensity over 120 as white and the rest black. The areas of the produced white blobs are calculated, and if multiple blobs big enough in comparison to the biggest blob are found, the image is considered to have multiple salient regions.
