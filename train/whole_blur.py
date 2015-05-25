import sys
import cv2
import glob
import numpy

from imgfilter.svm import SVM
from imgfilter.filters.whole_blur import get_input_vector


def train_svm(samples, labels):
    svm = SVM()
    svm.train(samples, labels)
    svm.save('whole_blur.yml')


def print_progress(n_samples, i):
    sys.stdout.write("\r%d%%" % (float(i) / n_samples * 100))
    sys.stdout.flush()


def get_images(path):
    return glob.glob(path + '/*.jpg') + glob.glob(path + '/*.png')


def collect_samples(blurred_images, unblurred_images):
    images = blurred_images + unblurred_images
    labels = ([1] * len(blurred_images)) + ([0] * len(unblurred_images))
    labels = numpy.array(labels, dtype=numpy.float32)

    samples = []
    for i, img in enumerate(images):
        image = cv2.imread(img)
        if image is None:
            continue
        samples.append(get_input_vector(image))
        print_progress(len(samples), i)

    return numpy.array(samples, dtype=numpy.float32), labels


if __name__ == '__main__':
    blurred_path = sys.argv[1]
    unblurred_path = sys.argv[2]

    try:
        blurred_images = get_images(blurred_path)
        unblurred_images = get_images(unblurred_path)
    except OSError:
        print 'Path to training images not found'
        sys.exit(1)

    samples, labels = collect_samples(blurred_images, unblurred_images)
    train_svm(samples, labels)
