Highlights
==========

Usage
-----
This filter recognizes images that contain one or more bright areas, for example the sun or spotlights from concerts. The difference to the exposure filter is that the bright area must be contiguous and the result is either 0: no highlights, or 1: one or more highlights.
The filter can be used by itself or in combination with the *qualipy.process* function by adding a **Highlights** class instance to the list of filters to be used.

.. currentmodule:: qualipy.filters.highlights
.. autoclass:: Highlights
   :members:

   .. automethod:: __init__

Performance
-----------

ROC curve:

.. image:: images/highlights/highlights_roc.png
   :width: 650px

How it works
------------

The image is first converted to grayscale and blurred to remove unwanted noise. Then the image is thresholded so that pixels with intensity over 250 are white and the rest are black, to help identify distinct highlighted areas. To count how many highlighted areas exist, OpenCV's findContours method is used to look for the areas in the thresholded image, and of the areas found, only those that are not either too small or rectangular are counted.

Examples:
---------

Sample image recognized as highlighted: (value: 1.0)

.. image:: images/highlights/positive.jpg
   :width: 200px

Sample image recognized as highlighted: (value: 1.0)
   
.. image:: images/highlights/positive_2.jpg
   :width: 200px

Sample image not recognized highlighted: (value: 0.00)

.. image:: images/highlights/negative.jpg
   :width: 200px

Some images where the intensity of the highlight isn't high enough or the highlights aren't large enough can produce false negatives such as following: 

.. image:: images/highlights/false_neg1.jpg
   :width: 300px

In some cases, the highlight isn't particularly noticeable for human eye, but the small continuous high-intensity area gives the image a positive result.

.. image:: images/highlights/false_pos1.jpg
   :width: 200px

.. image:: images/highlights/false_pos2.jpg
   :width: 200px
