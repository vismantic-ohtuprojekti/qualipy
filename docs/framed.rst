Frame detection
=======================


Usage
-----

The filter recognizes images that have frames added in them. At the moment only frames that surround the whole image are recognized.
The filter can be used in combination with the imgfilter.process function by adding a **Framed** class instance to the list of filters to be used.

ROC curve:

.. image:: images/exposure_roc_curve.png
   :width: 650px

How it works
------------

The filter first binarizes the image with adaptive thresholding and uses findContours-method from opencv to detect any rectangles in the image.

*"Contours can be explained simply as a curve joining all the continuous points (along the boundary), having same color or intensity. The contours are a useful tool for shape analysis and object detection and recognition."*

If the method returns four coordinates (for each corner of the image), they are analyzed to see if they form an rectangle, which is the case in framed images.


Examples:
---------

Sample images recognized as framed: (value: 1.0)

.. image:: images/framed/framed_3.jpg
   :width: 300px
   
.. image:: images/framed/framed_2.jpg
   :width: 300px

Sample images not recognized as framed: (value: 0.0)

.. image:: images/framed/negative_1.jpg
   :width: 200px

.. image:: images/framed/negative.jpg
   :width: 400px



