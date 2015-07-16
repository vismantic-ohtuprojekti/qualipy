Utilities
*********

Exif
====

.. automodule:: imgfilter.algorithms.exif
   :members:

SVM
===

.. automodule:: imgfilter.machine_learning.svm
   :members:

Flickr image downloader
=======================

Usage
-----

Flickr image downloader is in the project's script folder. It can be run from
the command line. It takes three arguments: how many images to download,
string of tags separated by commas and the path to the folder where to put the downloaded
images. If one wants to also get the exif data of an image, the system must have exiftool installed.
All downloaded images are in jpg format and of medium size. The script may fail to download
some images so every run doesn't always result to the given amount of images.

Example usage: *python flickr_photo_download.py 50 pattern patterns/*
Downloads 50 images from Flickr which have pattern as a tag.
