import tempfile
import pytest

from qualipy.utils.object_extraction import *


def test_object_extraction_lib_not_found_raises_exception():
    os.environ['SALIENCY_SO_PATH'] = 'fail'
    with pytest.raises(IOError):
        extract_object('/tests/images/lama.jpg')


def test_invalid_object_extraction_raises_exception():
    with tempfile.NamedTemporaryFile(suffix='.so') as temp:
        with open(temp.name, 'w') as out:
            out.write('fail')
        os.environ['SALIENCY_SO_PATH'] = temp.name
        with pytest.raises(OSError):
            extract_object('/tests/images/lama.jpg')
