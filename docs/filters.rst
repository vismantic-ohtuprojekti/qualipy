Filters
*******

Usage
=====
All filters can be used in combination with the imgfilter.process function by adding a corresponding class instance to the list of filters to be used. The filters return a float value between 0 and 1, where 0.0 indicates negative (for example 0.0 in blur detection indicates that the image is not blurred) and 1.0 indicates positive. When a prediction near 0.5 is returned, the filter is more uncertain about the classification.

List of filters
===============

.. toctree::
   :titlesonly:

   whole_blur
   blurred_context
   pattern_detection
   unconventional_size
   over_exposed
   small_object
   multiple_salient_regions
   hdr
   posterized
