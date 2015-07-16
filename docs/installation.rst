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

Usage examples
==============

Process function
----------------


Detect if the image or its background is blurred::

    import imgfilter
    from imgfilter.filters import *

    print imgfilter.process('image.jpg',
            [ WholeBlur(),
              BlurredContext(),
            ]
          )

Detect if each image on a list is blurred::

    import imgfilter
    from imgfilter.filters import *

    print imgfilter.process(['image1.jpg', 'image2.jpg'],
            [ WholeBlur(),
            ]
          )


Process request function
------------------------
The process_request function can be used to call the process function with
json data. The given json must be in the following format::

    { "images": [
        "a.jpg",
        "b.jpg"
        ],
        "filters": {
            "unconventional_size": {"max_aspect_ratio": 5}
        }
    }
