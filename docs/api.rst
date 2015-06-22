.. _api:

.. module:: imgfilter.filters

Filters
**************

Usage
=====
All filters can be used in combination with the imgfilter.process function by adding a corresponding class instance to the list of filters to be used

Return value
============
All filters return a float value where 0.0 indicates negative (for example 0.0 from blur detection indicates that image is not blurred)
and 1.0 indicates that positive. When prediction which is near 0.5 is returned filter is more uncertain about the classification.

.. include:: whole_blur.rst

.. include:: blurred_context.rst

.. include:: pattern_detection.rst

.. include:: over_exposed.rst

Utilities
*********

Exif
====

.. automodule:: imgfilter.analyzers.blur_detection.exif
   :members:

SVM
===

.. automodule:: imgfilter.machine_learning.svm
   :members:

Flickr image downloader
=======================

Usage
-----

Flickr image downloader is in the projects script folder. It can be ran from
command line. It takes three system parameters: how many images to download,
string of tags separated with comas and path to folder where to put the downloaded
images. If one want's to get also exif of image system must have exiftool installed.
All downloaded images are in jpg format and of medium size. Script may fail to download
some images so every run doesn't always result to given amount of images. Also Flickr tends
to give same images if when images with same tag are downloaded twice or more.

Example usage: *python flickr_photo_download 50 pattern /patterns*
Downloads 50 images from Flickr which have tag pattern.

Script that downloads  original photos works the same way except it doesn't guarantee that
images are in jpg format or which size images are in.
