# -*- coding: utf-8 -*- #
import numpy
import imgfilter
import os, glob, sys
from imgfilter.filters import *
from imgfilter.machine_learning.svm import SVM
from imgfilter.analyzers.blur_detection import exif

train = False # treenataanko vai luokitellaanko

svm = SVM()


if train:
    blur_dir = sys.argv[1]
    normal_dir = sys.argv[2]
    data = []
    luokat = []
    os.chdir(blur_dir)
    for img in glob.glob("*.jpg"):
        print img
        tags = exif.parse_exif(img)
        vectors = exif.get_image_vectors(tags)
        if vectors is None:
            continue
        else:
            data.append(vectors)
            luokat.append(1)
    
    os.chdir(normal_dir)
    for img in glob.glob("*.jpg"):
        print img
        tags = exif.parse_exif(img)
        vectors = exif.get_image_vectors(tags)
        if vectors is None:
            continue
        else:
            data.append(vectors)
            luokat.append(-1)
    print data
    data = numpy.asarray(data).astype(numpy.float32)
    luokat = numpy.asarray(luokat).astype(numpy.float32)

    svm.train(data, luokat) # <- data ja luokat pitää olla numpy-arrayita
    svm.save('data.yml')
else:
    # testailukoodia, lasketaan kansion kaikille kuville ennustus: 
    svm.load('data.yml')
    folder = sys.argv[1]
    os.chdir(folder)
    images = exif.get_images_in_folder()
    total_images = 0
    total_prediction = 0
    positives = 0
    negatives = 0
    for image in images:
        data = []
        tags = exif.parse_exif(image)
        vectors = exif.get_image_vectors(tags)
        if vectors is None:
            continue
        data.append(vectors)
        data = numpy.asarray(data).astype(numpy.float32)
        
        prediction = svm.predict(data)
        
        print image + ": " + str(prediction)
        if prediction > 1:
            positives += 1.0
        if prediction < 1:
            negatives += 1.0
        total_prediction += prediction
        total_images += 1
    print "avg: " + str(total_prediction / total_images)
    print "results: pos: " + str(positives / total_images)
    print "results: neg: " + str(negatives / total_images)
