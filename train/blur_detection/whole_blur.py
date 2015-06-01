import sys
import cv2
import glob
import numpy

from imgfilter.filters.whole_blur import get_input_vector
from imgfilter.machine_learning.svm import SVM


def train_svm(samples, labels):
    svm = SVM()
    svm.train(samples, labels)
    svm.save('whole_blur.yml')


def print_progress(n_samples, i):
    sys.stdout.write("\r%d%%" % (float(i) / n_samples * 100))
    sys.stdout.flush()


def get_images(path):
    extensions = ['.jpg', '.jpeg', '.JPG', '.png']

    images = []
    for ext in extensions:
        images.extend(glob.glob(path + '/*' + ext))
    return images


def collect_samples(blurred_images, unblurred_images):
    images = blurred_images + unblurred_images
    labels = ([1] * len(blurred_images)) + ([0] * len(unblurred_images))
    labels = numpy.array(labels, dtype=numpy.float32)

    samples = []
    for i, img in enumerate(images):
        image = cv2.imread(img, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        if image is None:
            continue
        samples.append(get_input_vector(image))
        print_progress(len(images), i)

    return numpy.array(samples, dtype=numpy.float32), labels


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write("Invalid number of arguments\n")
        sys.exit(1)

    blurred_path = sys.argv[1]
    unblurred_path = sys.argv[2]

    try:
        blurred_images = get_images(blurred_path)
        unblurred_images = get_images(unblurred_path)
    except OSError:
        sys.stderr.write("Path to training images not found\n")
        sys.exit(1)

    samples, labels = collect_samples(blurred_images, unblurred_images)
    train_svm(samples, labels)
