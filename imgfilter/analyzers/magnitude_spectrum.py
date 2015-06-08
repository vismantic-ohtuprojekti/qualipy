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
        :param image_path: path to the image file
        """
        self.data = count_magnitude_spectrum(image)


def logaritmic_tarnsformation2D(array_2D):
    """Performs a logarithmic transformation of a 2D array.

    :param array_2D: a 2D numpy matrix
    """
    c = 1 / numpy.log(1 + numpy.abs(numpy.amax(array_2D)))
    return c * numpy.log(1 + numpy.abs(array_2D))


def count_magnitude_spectrum(image):
    """Returns the magnitude spectrum of an image.

    :param image: image data as a numpy matrix
    """
    fft = numpy.fft.fft2(image)
    fshift = numpy.fft.fftshift(fft)
    return logaritmic_tarnsformation2D(fshift)
