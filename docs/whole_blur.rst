Blur detection
==============

Usage
-----

The filter can be used in combination with the imgfilter.process function by adding a **WholeBlur** class instance to the list of filters to be used.

Parameters
----------

.. currentmodule:: imgfilter.filters.whole_blur
.. autoclass:: WholeBlur

How it works
------------

Four focus measure algorithms that are described in *Analysis of focus measure operators for shape-from-focus* (Pattern recognition, 2012) by Pertuz et al are applied to the whole image. Focus measures measure the relative degree of focus of an image, and the implementations are based on their respective `MATLAB implementations <https://www.mathworks.com/matlabcentral/fileexchange/27314-focus-measure>`_.

The image is also divided into 5x5 equal-sized rectangles, and the focus measures are applied to these parts as well. As described by Mavridaki et al. in their paper *No-reference blur assessment in natural images using Fourier transform and spatial pyramids* (IEEE Int. Conf. on Image Processing (ICIP 2014), 2004), this is done to avoid the possibility of images having non-blurred parts misleading the focus measures.

The outcomes of the focus measure algorithms for the whole image and the smaller parts is concatenated into an input vector for a support vector machine used for the prediction. By default, the SVM has been trained with the `CERTH Image Blur Dataset <http://mklab.iti.gr/project/imageblur>`_. The final prediction is weighed by analyzing the probability of motion blur from the image's exif data, if possible.
