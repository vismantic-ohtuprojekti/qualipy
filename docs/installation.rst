.. _installation:


Installation
************

The library is packaged as an egg and can be installed by first installing
the necessary requirements and then issuing the following
command in the project's root folder::

    python setup.py install

Some filters use an object extraction algorithm provided in a file called
saliency.so. This file needs to be copied to the path imgfilter/data/object_extraction
before installation or the path to the file can be specified with an environmental
variable SALIENCY_SO_PATH.
