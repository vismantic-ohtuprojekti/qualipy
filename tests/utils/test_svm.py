import pickle
import tempfile

import numpy

from qualipy.utils.svm import *


def get_training_data():
    samples = numpy.array([numpy.array([i], dtype=numpy.float32)
                           for i in range(50)])
    labels = numpy.array(([1] * 25) + ([0] * 25), dtype=numpy.float32)
    return samples, labels


def test_can_train_svm():
    svm = SVM()
    svm.train(*get_training_data())


def test_can_save_and_load_model():
    svm = SVM()
    svm.train(*get_training_data())

    with tempfile.NamedTemporaryFile(suffix='.yml') as temp:
        svm.save(temp.name)
        svm.load(temp.name)


def test_can_be_saved_serialized():
    svm = SVM()
    svm.train(*get_training_data())

    with tempfile.NamedTemporaryFile(suffix='.dump') as temp:
        pickle.dump(svm, open(temp.name, 'wb'))


def test_can_be_loaded_serialized():
    svm = SVM()
    svm.train(*get_training_data())

    with tempfile.NamedTemporaryFile(suffix='.dump') as temp:
        pickle.dump(svm, open(temp.name, 'wb'))
        assert pickle.load(open(temp.name, 'rb')).__getstate__()
