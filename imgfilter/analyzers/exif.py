"""
Analyzer for reading the EXIF tags from an image.
Requires the exifread library.
"""

import exifread

from analyzer import Analyzer


class Exif(Analyzer):

    """Analyzer for reading the EXIF tags from an image"""

    def __init__(self):
        """Initializes an EXIF analyzer"""
        self.name = 'exif'
        self.data = None

    def run(self, image, image_path):
        """Runs the EXIF analyzer.

        :param image: the image matrix
        :type image: numpy.ndarray
        :param image_path: path to the image file
        :type image_path: str
        """
        self.data = parse_exif(image_path)


def parse_exif(image_path):
    """Parses the EXIF tags from an image.

    :param image_path: path to the image file
    :type image_path: str
    :returns: dict -- the exif tags
    """
    with open(image_path, 'rb') as image:
        return exifread.process_file(image, details=False)
