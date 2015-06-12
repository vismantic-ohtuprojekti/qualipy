class Analyzer(object):

    """An abstract class representing an analyzer"""

    def run(self, image_data):
        pass

    def get_copy(self):
        """Returns a copy of the data associated with
        the analyzer.
        """
        return self.data.copy()
