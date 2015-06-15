import cv2
import numpy


def LAPV(img):
    """Implements the LAPV focus measure algorithm.

    :param img: the image the measure is applied to as a numpy matrix
    """
    return numpy.std(cv2.Laplacian(img, cv2.CV_64F)) ** 2


def TENG(img):
    """Implements the TENG focus measure algorithm.

    :param img: the image the measure is applied to as a numpy matrix
    """
    gaussianX = cv2.Sobel(img, cv2.CV_64F, 1, 0)
    gaussianY = cv2.Sobel(img, cv2.CV_64F, 1, 0)
    return numpy.mean(gaussianX * gaussianX +
                      gaussianY * gaussianY)


def LAPM(img):
    """Implements the LAPM focus measure algorithm.

    :param img: the image the measure is applied to as a numpy matrix
    """
    kernel = numpy.array([-1, 2, -1])
    laplacianX = numpy.abs(cv2.filter2D(img, -1, kernel))
    laplacianY = numpy.abs(cv2.filter2D(img, -1, kernel.T))
    return numpy.mean(laplacianX + laplacianY)


def MLOG(img):
    """Implements the MLOG focus measure algorithm.

    :param img: the image the measure is applied to as a numpy matrix
    """
    return numpy.max(cv2.convertScaleAbs(cv2.Laplacian(img, 3)))
