import exifread

from analyzer import Analyzer


class Exif(Analyzer):

    """Analyzer for reading the exif tags from an image"""

    def __init__(self):
        """Initializes an exif analyzer"""
        self.name = 'exif'
        self.data = None

    def run(self, image, image_path):
        """Runs the exif analyzer

        :param image: image data as a numpy matrix
        :param image_path: path to the image file
        """
        self.data = parse_exif(image_path)


def parse_exif(image_path):
    """Parses the exif tags from an image.

    :param image_path: path to the image file
    """
    with open(image_path, 'rb') as image:
        return exifread.process_file(image, details=False)
