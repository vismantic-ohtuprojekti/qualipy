.. _installation:


Installation
************

The library is packaged as an egg and can be installed by first installing
the necessary requirements and then issuing the following
command in the project's root folder::

    python setup.py install

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
Process request function can be used call process function with
json data. Given json must be in this format:

{"filters": [{"whole_blur": {}},
  {"multiple_salient_regions": {}}],
  "images": ["image1.jpg", "image2.jpg"]}

Giving parameters to the process request function is not currently supported.
