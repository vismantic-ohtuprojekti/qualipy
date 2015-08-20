import pytest

from imgfilter.filters.fisheye import *

FISHEYE = 'tests/images/fisheye.jpg'
NON_FISHEYE = 'tests/images/lama.jpg'


# def test_recognizes_fisheye():
#     assert Fisheye().predict(FISHEYE)


# def test_doesnt_recognize_normal_image():
#     assert not Fisheye().predict(NON_FISHEYE)


def test_can_return_float():
    assert type(Fisheye().predict(FISHEYE, return_boolean=False)) != bool


def test_wrong_path_type_raises_exception():
    with pytest.raises(TypeError):
        Fisheye().predict(0)


# def test_training_with_too_few_images_causes_exception():
#     with pytest.raises(ValueError):
#         Fisheye().train([fisheye], [0])


# def test_training_with_invalid_number_of_labels_causes_exception():
#     with pytest.raises(ValueError):
#         Fisheye().train([fisheye], [])
