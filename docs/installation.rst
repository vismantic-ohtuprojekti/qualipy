.. _installation:


Installation
************

Requirements
------------

* OpenCV (version 2.4)
* Object extraction algorithm from https://github.com/assamite/CmCode

Optional requirements
---------------------

* tesseract-ocr (text detection)
* Numba (performance boost)

Installation
------------

The library is packaged as an egg and can be automatically installed using pip::

    pip install qualipy

or manually by issuing the following command in the project's root folder::

    python setup.py install

In order to use the text detection filter, `tesseract-ocr <https://code.google.com/p/tesseract-ocr/>`_ should be installed.

Some filters use an `object extraction algorithm <https://github.com/assamite/CmCode>`_ provided in a file called saliency.so. This file needs to be copied to the path qualipy/data/object_extraction before installation or the path to the file can be specified with an environmental variable SALIENCY_SO_PATH.

Additional speed-ups can be gained by installing the `Numba <http://numba.pydata.org/>`_ library. This speed-up is automatic and does not require any other action besides installing the library.
