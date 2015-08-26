import pytest

import qualipy
from qualipy.filters import *


TEST_IMG = 'tests/images/lama.jpg'
TEST_IMG2 = 'tests/images/framed.jpg'


def test_returns_true_for_no_filters():
    assert qualipy.process(TEST_IMG, []) == {TEST_IMG: True}


def test_processes_single_image_correctly():
    assert qualipy.process(TEST_IMG, [Framed()])


def test_processes_list_of_images_correctly():
    assert len(qualipy.process([TEST_IMG], [Framed()], None, True)) == 1


def test_images_exist_in_resulting_dict():
    res = qualipy.process([TEST_IMG, TEST_IMG2], [])
    assert TEST_IMG in res and TEST_IMG2 in res


def test_returns_True_when_all_filters_return_negative():
    assert qualipy.process(TEST_IMG, [Framed(), Pattern()])


def test_returns_False_when_some_filters_return_positive():
    assert qualipy.process(TEST_IMG2, [Framed(), Pattern()]) == {TEST_IMG2: False}


def test_returns_float_when_correct_parameter_is_set():
    assert qualipy.process(TEST_IMG, [Framed()], None, True)[TEST_IMG]['framed'] == 0. 
    assert qualipy.process(TEST_IMG, [Framed()], None, True, False)[TEST_IMG]['framed'] == 0.


def test_returns_boolean_for_each_filter_when_not_combining_results():
    assert qualipy.process(TEST_IMG, [Framed()], None, False, False)[TEST_IMG]['framed'] == 0. 


def test_ROI_can_be_None():
    assert qualipy.process(TEST_IMG, [Framed()], None)


def test_works_correctly_for_valid_ROI():
    assert qualipy.process(TEST_IMG, [Framed()], (0, 0, 100, 100))


def test_works_correctly_for_multiple_ROIs():
    assert qualipy.process([TEST_IMG, TEST_IMG2], [Framed()], [(0, 0, 100, 100), None])


def test_fails_for_invalid_type_ROI():
    with pytest.raises(TypeError):
        assert qualipy.process(TEST_IMG, [Framed()], 1)


def test_fails_for_invalid_length_ROI():
    with pytest.raises(TypeError):
        assert qualipy.process(TEST_IMG, [Framed()], (10, 10, 100))


def test_fails_for_invalid_amount_of_ROIs():
    with pytest.raises(ValueError):
        assert qualipy.process([TEST_IMG, TEST_IMG2], [Framed()],
                                 [(0, 0, 100, 100)])


def test_fails_for_invalid_images():
    with pytest.raises(TypeError):
        assert qualipy.process(0, [Framed()])


def test_works_with_magic_thresholds():
    assert qualipy.process(TEST_IMG,
                                 [Framed() == 1,
                                  Pattern() > 0.3,
                                  HDR() >= 0.5,
                                  UnconventionalSize() <= 16 / 9.,
                                  Exposure() != 1,
                                  Highlights() < 0.1
                                  ]) == {TEST_IMG: False} 


def test_process_request_works():
    json = r"""{ "images": { "tests/images/lama.jpg": null },
                 "filters": { "framed": { } } }
            """
    assert qualipy.process_request(json)[TEST_IMG]


def test_process_request_works_for_multiple_images():
    json = r"""{ "images": { "tests/images/lama.jpg": null,
                             "tests/images/framed.jpg": null },
                 "filters": { "framed": { } } }
            """
    assert len(qualipy.process_request(json)) == 2


def test_process_request_works_for_multiple_filters():
    json = r"""{ "images": { "tests/images/lama.jpg": null },
                 "filters": { "framed": { },
                              "exposure": { } } }
            """
    assert qualipy.process_request(json)[TEST_IMG]


def test_process_request_works_for_ROI():
    json = r"""{ "images": { "tests/images/lama.jpg": [0, 0, 200, 200] },
                 "filters": { "framed": { } } }
            """
    assert qualipy.process_request(json)[TEST_IMG]


def test_process_request_works_for_parameters():
    json = r"""{ "images": { "tests/images/lama.jpg": null },
                 "filters": { "framed": { } },
                 "combine_results": false }
            """
    assert type(qualipy.process_request(json)[TEST_IMG]) != bool


def test_process_request_works_for_filter_parameters():
    json = r"""{ "images": { "tests/images/framed.jpg": null },
                 "filters": { "framed": { "threshold": 1.01,
                                          "invert_threshold": true } } }
            """
    assert not qualipy.process_request(json)[TEST_IMG2]


def test_process_request_fails_for_invalid_json():
    json = r"""{ "images":  "tests/images/lama.jpg": null },
                 "filters": { "framed": { } } }
            """

    with pytest.raises(ValueError):
        qualipy.process_request(json)


def test_process_request_fails_for_no_images():
    json = r"""{ "filters": { "framed": { } } }"""

    with pytest.raises(ValueError):
        qualipy.process_request(json)


def test_process_request_fails_for_no_filters():
    json = r"""{ "images": { "tests/images/lama.jpg": null } }"""

    with pytest.raises(ValueError):
        qualipy.process_request(json)


def test_process_request_fails_for_invalid_filter():
    json = r"""{ "images": { "tests/images/framed.jpg": null },
                 "filters": { "fail": {  } } }
            """

    with pytest.raises(ValueError):
        qualipy.process_request(json)


def test_process_request_fails_for_invalid_parameters():
    json = r"""{ "images": { "tests/images/framed.jpg": null },
                 "filters": { "framed": { "x": 1.01 } } }
            """

    with pytest.raises(ValueError):
        qualipy.process_request(json)


def test_process_request_fials_for_invalid_ROI():
    json = r"""{ "images": { "tests/images/lama.jpg": [0, 0, 200] },
                 "filters": { "framed": { } } }
            """

    with pytest.raises(ValueError):
        qualipy.process_request(json)
