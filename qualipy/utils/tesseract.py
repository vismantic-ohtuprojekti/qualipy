import subprocess
import tempfile
import os


def img_to_str(tesseract_path, image):
    """Reads text in an image with tesseract-ocr

    :param tesseract_path: path to the tesseract executable
    :type tesseracth_path: str
    :param image: path to the input image
    :type image: str
    """
    if not os.path.isfile(image):
        raise OSError("image not found: %s" % image)

    with tempfile.NamedTemporaryFile(prefix="tess_") as outfile:
        try:
            status, err_str = __run_tesseract(tesseract_path,
                                              image, outfile.name)
            if status:
                raise OSError(err_str)
            with open(outfile.name + ".txt") as out:
                return out.read().strip()
        finally:
            __remove_file(outfile.name + ".txt")


def __run_tesseract(tesseract_path, infile, outfile):
    """Run tesseract process for given input file

    :param tesseract_path: path to the tesseract executable
    :type tesseracth_path: str
    :param infile: path to the input image
    :type infile: str
    :param outfile: path to the output file
    :type outfile: str
    """
    command = [tesseract_path, infile, outfile]
    tesseract = subprocess.Popen(command, stderr=subprocess.PIPE)
    return tesseract.wait(), tesseract.stderr.read()


def __remove_file(filename):
    try:
        os.remove(filename)
    except OSError:
        pass
