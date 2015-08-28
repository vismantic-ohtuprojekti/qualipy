.. _filters:

Filters
*******

Usage
=====

All filters can be used either separately or in combination with the *qualipy.process* function by adding a corresponding class instance to the list of filters to be used. The filters usually return a float value between 0 and 1, where 0.0 indicates negative (for example 0.0 in blur detection indicates that the image is not blurred) and 1.0 indicates positive. When a prediction near 0.5 is returned, the filter is more uncertain about the classification.

List of filters
===============

.. toctree::
   :titlesonly:

   blurred_context
   cross_processed
   exposure
   framed
   hdr
   highlights
   multiple_salient_regions
   pattern_detection
   posterized
   small_object
   text_detection
   unconventional_size
   whole_blur
