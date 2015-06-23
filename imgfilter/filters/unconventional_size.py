"""
Filter for detecting images that are of unconventional size.
Images with aspect ratio over 16:9 or 9:16 are considered
to be of unconventional size by default.
"""

from filter import Filter


class UnconventionalSize(Filter):

    """Filter for detecting images of unconventional size"""

    def __init__(self, max_aspect_ratio):
        """Initializese an unconventional size filter"""
        self.name = 'unconventional_size'
        self.parameters = {}
        self.max_aspect = max_aspect_ratio

    def required(self):
        return {'image'}

    def run(self):
        """Checks if the image is of unconventional size

        :returns: bool
        """
        height, width = self.parameters['image'].shape
        aspect_ratio = max(height, width) / float(min(height, width))
        return aspect_ratio > self.max_aspect
