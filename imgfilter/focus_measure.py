import cv2
import numpy


def LAPV(img):
    return numpy.std(cv2.Laplacian(img, cv2.CV_64F)) ** 2


def TENG(img):
    gaussianX = cv2.Sobel(img, cv2.CV_64F, 1, 0, 1)
    gaussianY = cv2.Sobel(img, cv2.CV_64F, 1, 0, 1)
    return numpy.mean(gaussianX * gaussianX +
                      gaussianY * gaussianY)


def LAPM(img):
    kernel = numpy.array([-1, 2, -1])
    laplacianX = numpy.abs(cv2.filter2D(img, -1, kernel))
    laplacianY = numpy.abs(cv2.filter2D(img, -1, kernel.T))
    return numpy.mean(laplacianX + laplacianY)


def MLOG(img):
    return numpy.max(cv2.convertScaleAbs(cv2.Laplacian(img, 3)))
