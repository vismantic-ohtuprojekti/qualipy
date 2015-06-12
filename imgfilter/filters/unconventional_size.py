from filter import Filter


class UnconventionalSize(Filter):

    def __init__(self, max_aspect_ratio):
        self.name = 'unconventional_size'
        self.parameters = {}
        self.max_aspect = max_aspect_ratio

    def required(self):
        return {'image'}

    def run(self):
        height, width = self.parameters['image'].shape
        aspect_ratio = max(height, width) / float(min(height, width))
        return aspect_ratio > self.max_aspect
