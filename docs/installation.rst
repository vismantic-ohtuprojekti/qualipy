.. _testing:


Installing projects
******************

The library is packaged as an egg and can be installed by first installing
the necessary requirements and then issuing the following
command in the project's root folder::

    python setup.py install

Usage examples
==============

Blur detection
--------------

Detect if an image is blurred::

    import imgfilter.filters.whole_blur as blur

    print blur.is_blurred('picture.jpg')
