.. _installation:


Installation
************

Requirements
============

* OpenCV
* Object detection algorithm from https://github.com/assamite/CmCode

Optional requirements
---------------------

* tesseract-ocr (text detection)
* Numba for performance boost


The library is packaged as an egg and can be automatically installed using pip::

    pip install qualipy

or manually by issuing the following command in the project's root folder::

    python setup.py install

Some filters use an `object extraction algorithm <https://github.com/assamite/CmCode>`_ provided in a file called saliency.so. This file needs to be copied to the path qualipy/data/object_extraction before installation or the path to the file can be specified with an environmental variable SALIENCY_SO_PATH.

Additional speed-ups can be gained by installing the `Numba <http://numba.pydata.org/>`_ library. This speed-up is automatic and does not require any other action besides installing the library.

Text detection also requires tesseract library in order to be used
