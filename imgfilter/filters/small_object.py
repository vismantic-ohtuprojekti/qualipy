from filter import Filter


class ObjectTooSmall(Filter):

    def __init__(self, min_ratio=0.05):
        self.name = 'object_too_small'
        self.parameters = {}
        self.min_ratio = min_ratio

    def required(self):
        return {'extract_object'}

    def run(self):
        obj = self.parameters['extract_object']
        ratio = white_pixels(obj) / float(obj.size)
        return ratio < self.min_ratio


def white_pixels(img):
    return len(img[img == 255])
