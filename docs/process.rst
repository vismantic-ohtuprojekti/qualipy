Process function
****************

Usage
-----

The process function can be used to run filters for
multiple images simultaneously. The process_request
can be used to handle calls to the process function
from a JSON request.

.. currentmodule:: qualipy.process
.. automodule:: qualipy.process
   :members:

Examples
--------

Example usage of the process function::

    qualipy.process(["1.jpg", ("2.jpg", (50, 50, 200, 200))],
                      [
                        HDR(threshold=0.6),
                        Pattern(),
                        BlurredContext(threshold=0.3,
                                       invert_threshold=True),
                      ],
                     )

Same command using magic thresholds::

    qualipy.process(["1.jpg", ("2.jpg", (50, 50, 200, 200))],
                      [
                        HDR() > 0.6,
                        Pattern(),
                        BlurredContext() < 0.3,
                      ],
                     )

Example JSON request for the process_request function::

    { "images": {
        "1.jpg": null,
        "2.jpg": [ 50, 50, 200, 200 ]
        },
    "filters": {
        "hdr": { 'threshold': 0.6 },
        "pattern": { },
        "blurred_context": { 'threshold': 0.3, 'invert_threshold': true }
    },
    "return_predictions": false,
    "combine_results": true,
    "sort_filters": true
    }
