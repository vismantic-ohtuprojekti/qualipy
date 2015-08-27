"""Various utility functions for dealing with images, such as
reading images as numpy arrays, resizing images or making them sharper."""

import os.path

import cv2
import numpy
import exifread

from utils import file_cache


@file_cache
def read_image(image_path, ROI=None):
    """Read an image from a file in grayscale

    :param image_path: path to the image file
    :type image_path: str
    :returns: numpy.ndarray
    """
    image = read_color_image(image_path, ROI)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


@file_cache
def read_color_image(image_path, ROI=None):
    """Read an image from a file in BGR format

    :param image_path: path to the image file
    :type image_path: str
    :returns: numpy.ndarray
    """
    if not (isinstance(image_path, str) or
            isinstance(image_path, unicode)):
        raise TypeError("image_path should be a string, not %s" %
                        type(image_path))

    if not os.path.isfile(image_path):
        raise IOError("Image not found: %s" % image_path)

    image = cv2.imread(image_path)
    if image is None:
        raise IOError("Unable to read image: %s" % image_path)

    return extract_ROI(image_path, image, ROI)


def extract_ROI(image_path, image, ROI):
    """Extract the region of interest out of an image

    :param image_path: path to the image file
    :type image_path: str
    :param image: the image matrix
    :type image: numpy.ndarray
    :returns: numpy.ndarray -- the region of interest
    """
    if ROI is None:
        return image

    if len(ROI) != 4:
        raise TypeError("ROI needs to be of length 4")

    x, y, w, h = ROI
    height, width, _ = image.shape

    if x < 0 or y < 0 or x + w > width or y + h > height:
        raise ValueError("Invalid dimensions for ROI for image: %s"
                         % image_path)

    return image[x:x + w, y:y + h]


def resize(image, size):
    """Resizes an image matrix so that the longest side
    of an image is the specified size at maximum.

    :param image: the image matrix
    :type image: numpy.ndarray
    :param size: the maximum size for one side of the image
    :type size: int
    :returns: numpy.ndarray
    """
    height, width = image.shape

    if max(height, width) <= size:
        return image

    ratio = max(height, width) / float(size)
    height /= ratio
    width /= ratio
    return cv2.resize(image, (int(height), int(width)))


def read_exif_tags(image_path):
    """Parses the EXIF tags from an image.

    :param image_path: path to the image file
    :type image_path: str
    :returns: dict -- the exif tags
    """
    with open(image_path, 'rb') as image:
        return exifread.process_file(image, details=False)


def reduce_colors(image, colors):
    """Reduces the number of colors in a given image to certain
    amount. The algorithm uses the k-nearest neighbors method to
    do this. The given image must have colors, meaning three color
    channels. The algorithm is taken from
    "http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans
    /py_kmeans_opencv/py_kmeans_opencv.html"

    :param image: the image to process (must have three channels)
    :type image: numpy.ndarray
    :param colors: how many colors the final image should have
    :type colors: int
    :returns: numpy.ndarray
    """
    Z = image.reshape((-1, 3)).astype(numpy.float32)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(data=Z, K=colors, criteria=criteria,
                                    attempts=10, flags=cv2.KMEANS_PP_CENTERS,
                                    bestLabels=None)

    center = numpy.uint8(center)
    return center[label.flatten()].reshape(image.shape)


def sharpen(image):
    """Sharpens an image.

    :param image: the image matrix
    :type image: numpy.ndarray
    :returns: numpy.ndarray
    """
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    return cv2.addWeighted(image, 1.5, blur, -0.5, 0)


def logarithmic_transformation2D(array_2D):
    """Performs a logarithmic transformation of a matrix.

    :param array_2D: a numpy matrix
    :type array_2D: numpy.ndarray
    :returns: numpy.ndarray
    """
    c = 1 / numpy.log(1 + numpy.abs(numpy.amax(array_2D)))
    return c * numpy.log(1 + numpy.abs(array_2D))


def count_magnitude_spectrum(image):
    """Returns the magnitude spectrum of an image.

    :param image: the image matrix
    :type image: numpy.ndarray
    :returns: numpy.ndarray
    """
    fft = numpy.fft.fft2(image)
    fshift = numpy.fft.fftshift(fft)
    return logarithmic_transformation2D(fshift)
