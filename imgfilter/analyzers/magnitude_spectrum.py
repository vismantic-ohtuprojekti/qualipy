import numpy as np

def logaritmic_tarnsformation2D(array_2D):
    c = 1 / np.log(1 + np.abs(np.amax(array_2D)))
    return c * np.log(1 + np.abs(array_2D))

def count_magnitude_spectrum(image):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    return logaritmic_tarnsformation2D(fshift)

class MagnitudeSpectrum(Analyzer):
    def __init__(self):
        name = 'magnitude_spectrum'
        data = None

    def run(self, image_data):
        self.data = count_magnitude_spectrum(image_data['image'])
