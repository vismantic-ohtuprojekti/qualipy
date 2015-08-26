import subprocess
import tempfile
import os
import sys

def run_tesseract(tesseract_path, infile, outfile):
    command = [tesseract_path, infile, outfile]
    proc = subprocess.Popen(command, stderr=subprocess.PIPE)
    return (proc.wait(), proc.stderr.read())

def img_to_str(tesseract_path, image):
    """reads text in a image with the tesseract-ocr."""
    with tempfile.NamedTemporaryFile(prefix="tess_") as outfile:
        try:
            status, err_str = run_tesseract(tesseract_path, image, outfile.name)
            if status:
                errors = get_errors(error_string)
                raise TesseractErr(status, errors)
            with open(outfile.name + ".txt") as out:
                return out.read().strip()
        finally:
            cleanup(outfile.name + ".txt")
           
def cleanup(filename):
    try:
        os.remove(filename)
    except OSError:
        pass 
        
def get_errors(error_string):
    lines = error_string.splitlines()
    error_lines = tuple(line for line in lines if line.find('Error') >= 0)
    if len(error_lines) > 0:
        return '\n'.join(error_lines)
    else:
        return error_string.strip()
        
class TesseractErr(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message
        self.args = (status, message)
    
if __name__ == '__main__':
    print read_image('tesseract', sys.argv[1])
