import pytest

import imgfilter
from imgfilter.filters import *


TEST_IMG = 'tests/images/lama.jpg'
TEST_IMG2 = 'tests/images/framed.jpg'


def test_returns_true_for_no_filters():
    assert imgfilter.process(TEST_IMG, []) == True


def test_processes_single_image_correctly():
    assert imgfilter.process(TEST_IMG, [Framed()])


def test_processes_list_of_images_correctly():
    assert len(imgfilter.process([TEST_IMG], [Framed()], True)) == 1


def test_images_exist_in_resulting_dict():
    res = imgfilter.process([TEST_IMG, TEST_IMG2], [])
    assert TEST_IMG in res and TEST_IMG2 in res


def test_returns_True_when_all_filters_return_negative():
    assert imgfilter.process(TEST_IMG, [Framed(), Pattern()])


def test_returns_False_when_some_filters_return_positive():
    assert imgfilter.process(TEST_IMG2, [Framed(), Pattern()]) == False


def test_returns_float_when_correct_parameter_is_set():
    assert imgfilter.process(TEST_IMG, [Framed()], True)['framed'] == 0.
    assert imgfilter.process(TEST_IMG, [Framed()], True, False)['framed'] == 0.


def test_returns_boolean_for_each_filter_when_not_combining_results():
    assert imgfilter.process(TEST_IMG, [Framed()], False, False)['framed'] == False


def test_ROI_can_be_None():
    assert imgfilter.process((TEST_IMG, None), [Framed()])


def test_works_correctly_for_valid_ROI():
    assert imgfilter.process((TEST_IMG, (0, 0, 100, 100)), [Framed()])


def test_fails_for_invalid_type_ROI():
    with pytest.raises(TypeError):
        assert imgfilter.process((TEST_IMG, 10), [Framed()])


def test_fails_for_invalid_length_ROI():
    with pytest.raises(TypeError):
        assert imgfilter.process((TEST_IMG, (10, 10, 100)), [Framed()])


def test_fails_for_invalid_images():
    with pytest.raises(TypeError):
        assert imgfilter.process(0, [Framed()])


def test_works_with_magic_thresholds():
    assert imgfilter.process(TEST_IMG,
                             [Framed() > 0.1, Pattern() > 0.3, HDR() > 0.5])
