Text detection
==============

Usage
-----

The filter can be used by itself or in combination with the imgfilter.process function by adding a **TextDetection** class instance to the list of filters to be used. Uses `tesseract-ocr <https://code.google.com/p/tesseract-ocr/>`_ to find text in images. If tesseract-ocr finds more than one character of text in the image, the image is predicted to contain text.

.. currentmodule:: qualipy.filters.text_detection
.. autoclass:: TextDetection
   :members:

   .. automethod:: __init__
