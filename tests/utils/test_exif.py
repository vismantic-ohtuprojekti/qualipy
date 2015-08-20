from imgfilter.utils.exif import *

EXIF = parse_exif('tests/images/exif.JPG')
NOEXIF = parse_exif('tests/images/lama.JPG')

def test_analyze_background_blur():
    res = analyze_background_blur(EXIF)
    assert 0.4 < res
    assert 0.6 > res

def test_analyze_picture_exposure():
    res = analyze_picture_exposure(EXIF)
    assert 0.6 > res
    assert 0.4 < res

def test_correctly_parse_exif_data():
    # Exposure
    assert 1.0 / 75 > get_exposure_value(EXIF)
    assert 1.0 / 85 < get_exposure_value(EXIF)
    
    # Focal length
    assert 17 < get_focal_value(EXIF)
    assert 19 > get_focal_value(EXIF)
    
    # ISO 
    assert 80 == get_iso_value(EXIF)

    # Aperture
    assert 5 == get_aperture_value(EXIF)

def test_parsing_returns_none_if_not_found():
    assert None == get_exposure_value(NOEXIF)
    assert None == get_focal_value(NOEXIF)
    assert None == get_iso_value(NOEXIF)
    assert None == get_aperture_value(NOEXIF)
    
def test_exposure_max_values():
    tags = {'EXIF ExposureTime': '15', 'EXIF FocalLength': '50', 'EXIF ApertureValue': '1'}
    assert 1.0 == analyze_picture_exposure(tags)

    tags = {'EXIF ExposureTime': '1', 'EXIF FocalLength': '15', 'EXIF ApertureValue': '8'}
    assert 1.0 == analyze_picture_exposure(tags)

    tags = {'EXIF ExposureTime': '1/4', 'EXIF FocalLength': '15', 'EXIF ApertureValue': '8'}
    assert 1.0 == analyze_picture_exposure(tags)


def test_exposure_min_values():
    tags = {'EXIF ExposureTime': '1/8000', 'EXIF FocalLength': '50', 'EXIF ApertureValue': '1'}
    assert 0.0 == analyze_picture_exposure(tags)

    tags = {'EXIF ExposureTime': '1/4000', 'EXIF FocalLength': '15', 'EXIF ApertureValue': '8'}
    assert 0.0 == analyze_picture_exposure(tags)

    tags = {'EXIF ExposureTime': '1/2000', 'EXIF FocalLength': '15', 'EXIF ApertureValue': '8'}
    assert 0.0 == analyze_picture_exposure(tags)


def test_hyperfocal_max_values():
    tags = {'EXIF ExposureTime': '1/8000', 'EXIF FocalLength': '100', 'EXIF ApertureValue': '4'}
    assert 1.0 == analyze_background_blur(tags)

    tags = {'EXIF ExposureTime': '1/4000', 'EXIF FocalLength': '50', 'EXIF ApertureValue': '1'}
    assert 1.0 == analyze_background_blur(tags)

    tags = {'EXIF ExposureTime': '1/2000', 'EXIF FocalLength': '200', 'EXIF ApertureValue': '8'}
    assert 1.0 == analyze_background_blur(tags)


def test_hyperfocal_min_values():
    tags = {'EXIF ExposureTime': '1/8000', 'EXIF FocalLength': '5', 'EXIF ApertureValue': '2'}
    assert 0.2 < analyze_background_blur(tags)

    tags = {'EXIF ExposureTime': '1/4000', 'EXIF FocalLength': '30', 'EXIF ApertureValue': '16'}
    assert 0.2 < analyze_background_blur(tags)

    tags = {'EXIF ExposureTime': '1/2000', 'EXIF FocalLength': '10', 'EXIF ApertureValue': '8'}
    assert 0.2 < analyze_background_blur(tags)
