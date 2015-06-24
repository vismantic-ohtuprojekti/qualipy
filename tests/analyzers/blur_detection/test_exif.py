from imgfilter.analyzers.blur_detection import exif


def test_exposure_max_values():
    tags = {'EXIF ExposureTime': '15', 'EXIF FocalLength': '50', 'EXIF ApertureValue': '1'}
    assert 1.0 == exif.analyze_picture_exposure(tags)

    tags = {'EXIF ExposureTime': '1', 'EXIF FocalLength': '15', 'EXIF ApertureValue': '8'}
    assert 1.0 == exif.analyze_picture_exposure(tags)

    tags = {'EXIF ExposureTime': '1/4', 'EXIF FocalLength': '15', 'EXIF ApertureValue': '8'}
    assert 1.0 == exif.analyze_picture_exposure(tags)


def test_exposure_min_values():
    tags = {'EXIF ExposureTime': '1/8000', 'EXIF FocalLength': '50', 'EXIF ApertureValue': '1'}
    assert 0.0 == exif.analyze_picture_exposure(tags)

    tags = {'EXIF ExposureTime': '1/4000', 'EXIF FocalLength': '15', 'EXIF ApertureValue': '8'}
    assert 0.0 == exif.analyze_picture_exposure(tags)

    tags = {'EXIF ExposureTime': '1/2000', 'EXIF FocalLength': '15', 'EXIF ApertureValue': '8'}
    assert 0.0 == exif.analyze_picture_exposure(tags)


def test_hyperfocal_max_values():
    tags = {'EXIF ExposureTime': '1/8000', 'EXIF FocalLength': '100', 'EXIF ApertureValue': '4'}
    assert 1.0 == exif.analyze_background_blur(tags)

    tags = {'EXIF ExposureTime': '1/4000', 'EXIF FocalLength': '50', 'EXIF ApertureValue': '1'}
    assert 1.0 == exif.analyze_background_blur(tags)

    tags = {'EXIF ExposureTime': '1/2000', 'EXIF FocalLength': '200', 'EXIF ApertureValue': '8'}
    assert 1.0 == exif.analyze_background_blur(tags)


def test_hyperfocal_min_values():
    tags = {'EXIF ExposureTime': '1/8000', 'EXIF FocalLength': '5', 'EXIF ApertureValue': '2'}
    assert 0.2 < exif.analyze_background_blur(tags)

    tags = {'EXIF ExposureTime': '1/4000', 'EXIF FocalLength': '30', 'EXIF ApertureValue': '16'}
    assert 0.2 < exif.analyze_background_blur(tags)

    tags = {'EXIF ExposureTime': '1/2000', 'EXIF FocalLength': '10', 'EXIF ApertureValue': '8'}
    assert 0.2 < exif.analyze_background_blur(tags)
