import cv2
import numpy as np

from filter import Filter

from matplotlib import pyplot as plt

# pkg-config --libs opencv for C++ compilation

# Put auto canny zero parameter here
def simplifyImage(image):
    edges = cv2.Canny(image,100,200)

    plt.subplot(121),plt.imshow(image, cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges, cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()


# This still needs imrovement for edges
def slide_window(image, widht, height, step):
    windows = []

    #print 'height iter: ', int(image.shape[0] / height)
    #print 'width iter: ', int(image.shape[1] / widht)

    for y in range(0, int(image.shape[0] - height), step):
        for x in range(0, int(image.shape[1] - widht), step):
            window = image[y:y+height, x:x+widht]
            windows.append(window)

    return windows


def draw_slides(image):
    print 'calculating sides'
    windows = slide_window(image, 100, 120, 40)
    print 'drawing slides: ', len(windows)
    for i in range(0, len(windows)):
        cv2.imshow('Silide: ' + str(i), windows[i])
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def detext_text(image):
    start_width = int(0.05 * image.shape[1])
    start_height = int(0.05 * image.shape[0])
    windows = slide_window(image, start_width, start_height, int(0.05 * image.shape[1]))

    print 'total slides: ', len(windows)

    for i in range(0, len(windows)):
        simplifyImage(windows[i])



class TextDetection(Filter):
    name = 'text_detection'
    speed = 10

    def __init__(self, threshold=0.5, invert_threshold=False):
        super(TextDetection, self).__init__(threshold, invert_threshold)

    def predict(self, image_path, return_boolean=True, ROI=None):
        if return_boolean:
            return self.boolean_result(0.0)
        return 0.0
