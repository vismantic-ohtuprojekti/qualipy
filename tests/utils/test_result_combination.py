from qualipy.utils.result_combination import *


def test_collective_result_for_two_uncertain():
    assert abs(0.5 - collective_result([0.2, 0.8], 0)) <= 0.0001


def test_collective_result_for_one_certain():
    assert abs(0.8 - collective_result([0.4, 0.8], 0.3)) <= 0.0001


def test_collective_result_for_two_certain():
    assert abs(0.85 - collective_result([0.8, 0.9], 0.3)) <= 0.0001
