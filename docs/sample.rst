.. _sample:


Sample run
**********

Running all currently implemented filters for the image

.. image:: images/lena.jpg
   :width: 300px

gives the result::

    {'blurred_context': 1, 'hdr': 1, 'cross_processed': 1,
     'highlights': 0, 'object_too_small': 0.27240753173828125,
     'framed': 0, 'unconventional_size': 1.0,
     'multiple_salient_regions': 0.051772484864809787,
     'pattern': 0.3037661050545094, 'posterized': 0.36023458233103156, 
     'whole_blur': 0, 'exposure': 1}

Using a threshold of 0.5, we can see that the image would be classified as blurred_context, hdr, cross_processed and exposure, of which hdr and exposure would be false positives. The return values for unconventional_size and object_too_small indicate that the picture's width and height are the same and that the detected object occupies about 27% of the image's area, respectively.
