import numpy

from analyzer import Analyzer


class MagnitudeSpectrum(Analyzer):

    def __init__(self):
        self.name = 'magnitude_spectrum'
        self.data = None

    def run(self, image, image_path):
        self.data = count_magnitude_spectrum(image)


def logaritmic_tarnsformation2D(array_2D):
    c = 1 / numpy.log(1 + numpy.abs(numpy.amax(array_2D)))
    return c * numpy.log(1 + numpy.abs(array_2D))


def count_magnitude_spectrum(image):
    fft = numpy.fft.fft2(image)
    fshift = numpy.fft.fftshift(fft)
    return logaritmic_tarnsformation2D(fshift)
