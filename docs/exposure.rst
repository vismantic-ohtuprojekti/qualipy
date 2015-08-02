Exposure
========

Usage
-----

The filter can be used by itself or in combination with the *imgfilter.process* function by adding a **Exposure** class instance to the list of filters to be used.

.. currentmodule:: imgfilter.filters.exposure
.. autoclass:: Exposure
   :members:

   .. automethod:: __init__

Performance
-----------

ROC curve:

.. image:: images/exposure_roc_curve.png
   :width: 650px

How it works
------------

The filter converts the image to grayscale and makes a histogram of it. It then calculates the percentage of pixels with greater than 250 intensity and normalizes the result (result * 50) to a float between 0 and 1. If there's none over 250 then the picture is recognized under exposed.

Examples:
---------

Sample image recognized as over-exposured: (value: 1.0)

.. image:: images/over_exposure_sample.jpg
   :width: 200px

Sample image recognized as under-exposured: (value: 1.0)
   
.. image:: images/under_exposure_sample.jpg
   :width: 200px

Sample image not recognized as under- or over-exposured: (value: 0.31)

.. image:: images/exposure_sample_good.jpg
   :width: 200px


