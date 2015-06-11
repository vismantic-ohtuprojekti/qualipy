import sys
import cv2
import glob
import numpy

from imgfilter.machine_learning.svm import SVM

import imgfilter.filters.whole_blur
import imgfilter.filters.blurred_context
import imgfilter.filters.low_resolution


FILTERS = \
    {'--whole_blur': imgfilter.filters.whole_blur.get_input_vector,
     '--blurred_context': imgfilter.filters.blurred_context.get_input_vector,
     '--low_resolution': imgfilter.filters.low_resolution.get_input_vector
     }


def train_svm(samples, labels, save_path):
    svm = SVM()
    svm.train(samples, labels)
    svm.save(save_path)


def print_progress(n_samples, i):
    sys.stdout.write("\r%d%%" % (float(i) / n_samples * 100))
    sys.stdout.flush()


def get_images(path):
    extensions = ['.jpg', '.jpeg', '.JPG', '.png']

    images = []
    for ext in extensions:
        images.extend(glob.glob(path + '/*' + ext))
    return images


def collect_samples(get_input, positive_images, negative_images):
    images = positive_images + negative_images
    labels = ([1] * len(positive_images)) + ([0] * len(negative_images))
    labels = numpy.array(labels, dtype=numpy.float32)

    samples = []
    for i, img in enumerate(images):
        image = cv2.imread(img, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        if image is None:
            continue
        samples.append(get_input(image))
        print_progress(len(images), i)

    return numpy.array(samples, dtype=numpy.float32), labels


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.stderr.write('Invalid number of arguments\n')
        sys.exit(1)

    filter_name = sys.argv[1]
    positive_path = sys.argv[2]
    negative_path = sys.argv[3]

    if filter_name not in FILTERS:
        sys.stderr.write('Invalid filter\n')
        sys.exit(2)

    try:
        positive_images = get_images(positive_path)
        negative_images = get_images(negative_path)
    except OSError:
        sys.stderr.write('Invalid path to training images\n')
        sys.exit(3)

    samples, labels = collect_samples(FILTERS[filter_name],
                                      positive_images, negative_images)
    train_svm(samples, labels, filter_name[2::] + '.yml')
