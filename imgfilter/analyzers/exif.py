import exifread

from analyzer import Analyzer


class Exif(Analyzer):

    def __init__(self):
        self.name = 'exif'
        self.data = None

    def run(self, image, image_path):
        self.data = parse_exif(image_path)


def parse_exif(image_path):
    with open(image_path, 'rb') as image:
        return exifread.process_file(image, details=False)
