.. _examples:


Usage examples
**************

Detect if an image is blurred::

    >>> from qualipy.filters import WholeBlur
    >>> wb = WholeBlur()
    >>> wb.predict('image.jpg', ROI=(20, 20, 100, 100))
    True

Use the process function to detect if each image on a list is blurred::

    >>> import qualipy
    >>> from qualipy.filters import *
    >>> qualipy.process(['image1.jpg', 'image2.jpg'], [WholeBlur()])
    {'image1.jpg': False, 'image2.jpg': True}


Use the process function to detect if the image or its background is blurred::

    >>> import qualipy
    >>> from qualipy.filters import *
    >>> qualipy.process('image.jpg',
    ...   [ WholeBlur(),
    ...     BlurredContext(),
    ...   ],
    ...   return_predictions=True
    ... )
    {'whole_blur': 0.162358723895, 'blurred_context': 0.884614553712}


Use the process function to detect if an image is a HDR image with over 90% probability and
has a frame with under 10% probability::

    >>> import qualipy
    >>> from qualipy.filters import *
    >>> qualipy.process('image.jpg',
    ...   [ HDR() > 0.9,
    ...     Framed() < 0.1
    ...   ]
    ... )
    False


Use the process_request function to run filters from a JSON request::

    >>> import qualipy
    >>> json = r"""{ "images": {
    ...                "1.jpg": null,
    ...                "2.jpg": [ 50, 50, 200, 200 ]
    ...              },
    ...              "filters": {
    ...                "hdr": { 'threshold': 0.6 },
    ...                "pattern": { },
    ...                "blurred_context": { 'threshold': 0.3, 'invert_threshold': true }
    ...              },
    ...              "return_predictions": false,
    ...              "combine_results": true,
    ...              "sort_filters": true
    ...              }
    ...         """
    >>> qualipy.process_request(json)
    False

Train the whole_blur filter::

    >>> import glob, qualipy
    >>> from qualipy.filters import *
    >>> positives = glob.glob('positives/*.jpg')
    >>> negatives = glob.glob('negatives/*.jpg')
    >>> labels = ([1] * len(positives)) + ([0] * len(negatives))
    >>> wb = WholeBlur()
    >>> wb.train(positives + negatives, labels, 'new.yml')
