import imgfilter
from imgfilter.filters import *


def test_returns_empty_dict_for_no_filters():
    assert imgfilter.process('tests/images/lama.jpg', []) == dict()


def test_processes_single_image_correctly():
    assert 'unconventional_size' in \
        imgfilter.process('tests/images/lama.jpg', [UnconventionalSize()])


def test_processes_list_of_images_correctly():
    assert len(imgfilter.process(['tests/images/lama.jpg'],
                                 [UnconventionalSize()])) == 1
