"""
Analyzer for calculating the magnitude spectrum of an image using
Fast Fourier Transformation and applying logarithmic transformation.
"""

import numpy

from analyzer import Analyzer


class MagnitudeSpectrum(Analyzer):

    """Analyzer for calculating the magnitude spectrum of an image"""

    def __init__(self):
        """Initializes a magnitude spectrum analyzer"""
        self.name = 'magnitude_spectrum'
        self.data = None

    def run(self, image, image_path):
        """Runs the magnitude spectrum analyzer

        :param image: image data as a numpy matrix
        :type image: numpy.ndarray
        :param image_path: path to the image file
        :type image_path: str
        """
        self.data = count_magnitude_spectrum(image)


def logaritmic_tarnsformation2D(array_2D):
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
    return logaritmic_tarnsformation2D(fshift)
