Cross Processed
===============

Usage
-----

The filter can be used by itself or in combination with the *imgfilter.process* function by adding a **Posterized** class instance to the list of filters to be used.

.. currentmodule:: imgfilter.filters.cross_processed
.. autoclass:: CrossProcessed
   :members:

   .. automethod:: __init__

How it works
------------
In order to detect cross processed image filter first separates both 20 % of the brigthest and
the darkest pixels in the image. This is useful since usually in cross processed image all
dark areas have some same color (not black) and also bright areas have some same color (not white).
In order to avoid black and white colors they are removed from darkest and brigthest areas.

After this tree values are calculated for both dark and bright areas. Value which indicates
normal image is prefered over cross processed since normal image can in this analyse look
partly cross processed. Tree calculated values are average sharpness of the peaks, area size
where there are lots of pixels and standard deviation.

Special Cases
-------------
Cross processed detection has some problems detecting images which contain red as one of the magnified colors. This is because red is both at the start and at the end of the hue histogram when trying to find magnified areas red often is interepted as two areas instead of one.

.. image:: images/cross_processed_roc_curve.png

roc curve of cross processed image filter
