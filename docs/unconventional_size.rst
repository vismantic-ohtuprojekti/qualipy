Unconventional size
===================

Usage
-----

The filter can be used in combination with the imgfilter.process function by adding a **UnconventialSize** class instance to the list of filters to be used.

Parameters
----------

.. currentmodule:: imgfilter.filters.unconventional_size
.. autoclass:: UnconventionalSize

The **max_aspect** parameter is used to define the point where higher values than the max_aspect are considered unconventional sized. For example, the default value max_aspect = 16. / 9. indicates that images with an aspect ratio over 16:9 or 9:16 are to be filtered.
