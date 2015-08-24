from ..utils.pytesseract import img_to_str

from filter import Filter


class TextDetection(Filter):

    name = 'text_detection'
    speed = 3

    def __init__(self, threshold=0.5, invert_threshold=False):
        super(TextDetection, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True, ROI=None):
        
        if len(img_to_str('tesseract', image_path)) > 1:
            prediction = 1.0
        else:
            prediction = 0.0

        if return_boolean:
            return self.boolean_result(prediction)
        return prediction
