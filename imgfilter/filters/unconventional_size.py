from filter import Filter


class UnconventionalSize(Filter):

    def __init__(self, min_aspect, max_aspect):
        self.name = 'unconventional_size'
        self.parameters = {}
        self.min_aspect = min_aspect
        self.max_aspect = max_aspect

    def required(self):
        return {'image'}

    def run(self):
        height, width = self.parameters['image'].shape
        aspect_ratio = max(height, width) / float(min(height, width))
        return aspect_ratio < self.min_aspect or aspect_ratio > self.max_aspect
