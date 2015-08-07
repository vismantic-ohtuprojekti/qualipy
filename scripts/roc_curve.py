import sys
import glob
import numpy
import pylab

import imgfilter
from imgfilter.filters import *


def get_images(path):
    extensions = ['.jpg', '.jpeg', '.JPG', '.png']

    images = []
    for ext in extensions:
        images.extend(glob.glob(path + '/*' + ext))
    return images


if __name__ == '__main__':
    positive_path = sys.argv[1]
    negative_path = sys.argv[2]

    positive_images = get_images(positive_path)
    negative_images = get_images(negative_path)

    res = imgfilter.process(positive_images, [Posterized()], True)
    fst = numpy.array([x['posterized'] for x in res.values()],
                      dtype=numpy.float32)
    res = imgfilter.process(negative_images, [Posterized()], True)
    snd = numpy.array([x['posterized'] for x in res.values()],
                      dtype=numpy.float32)

    thresholds = numpy.arange(-0.001, 1.001, 0.001)

    y1, y2 = [], []
    for thresh in thresholds:
        y1.append(len(fst[fst > thresh]) / float(len(positive_images)))
        y2.append(len(snd[snd <= thresh]) / float(len(negative_images)))

    y1, y2 = numpy.array(y1), numpy.array(y2)
    pylab.xlabel('False positive rate')
    pylab.ylabel('True positive rate')
    pylab.ylim(0, 1)
    pylab.plot(1 - y2, y1)
    pylab.legend(loc=3)
    pylab.show()
