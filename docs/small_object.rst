Object too small
================

Usage
-----

The filter can be used in combination with the imgfilter.process function by adding a **ObjectTooSmall** class instance to the list of filters to be used.

Parameters
----------

.. currentmodule:: imgfilter.filters.small_object
.. autoclass:: ObjectTooSmall

The **min_ratio** parameter is used to define the minimum size for an object as the ratio of the size of the image. Sizes below this ratio are considered to be small. The default ratio is 0.05.
