import statistic_common

import cv2
import numpy as np
from matplotlib import pyplot as plt


def mark_all_points_outside_circle(array_2D, radii, image):
    center = np.array((array_2D.shape[0]/2.0, array_2D.shape[1]/2.0))

    for x in range(0, array_2D.shape[0]):
        for y in range(0, array_2D.shape[1]):
            distance_from_center = np.abs(np.linalg.norm(center - np.array((x,y))))

            if distance_from_center > radii:
                array_2D[x,y] = 1

    plt.figure('Test')
    plt.subplot(121),plt.imshow(array_2D, cmap = 'gray')
    plt.title('Magnitude spectrum'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(image, cmap = 'gray')
    plt.title('Color reduced image')
    plt.show()
    return array_2D


def logaritmic_tarnsformation2D(array_2D):
    c = 1 / np.log(1 + np.abs(np.amax(array_2D)))
    return c * np.log(1 + np.abs(array_2D))


def count_magnitude_spectrum(image):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    return logaritmic_tarnsformation2D(fshift)


def reduce_colors(image, colors):
    Z = image.reshape((-1,3))

    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = colors
    ret,label,center=cv2.kmeans(Z,K,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((image.shape))
    return res2


def pattern_regonition(image_path):
    # Turn into gray scale
    image = cv2.imread(image_path)
    image = reduce_colors(image, 2)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Count magnitude spectrum
    magnitude_spectrum = count_magnitude_spectrum(image)

    # Center of the image
    center = np.array((magnitude_spectrum.shape[0]/2.0, magnitude_spectrum.shape[1]/2.0))

    all_distances = np.array([])

    for x in xrange(0, magnitude_spectrum.shape[0]):
        for y in xrange(0, magnitude_spectrum.shape[1]):
            # Count distance from the center of the image
            distance_from_center = np.abs(np.linalg.norm(center - np.array((x,y))))

            # Make magnitude spectrum to contain only high values
            # and count all non zero points
            if magnitude_spectrum[x,y] > 0.70:
                magnitude_spectrum[x,y] = 2
                all_distances = np.append(all_distances, distance_from_center)
            else:
                magnitude_spectrum[x,y] = 0


    all_distances = statistic_common.remove_anomalies(all_distances, 0.4)
    max_distances = statistic_common.get_max_values(all_distances, 20)

    max_distance_avg = statistic_common.avarage(max_distances)
    magnitude_spectrum = mark_all_points_outside_circle(magnitude_spectrum, max_distance_avg, image)

    all_points = np.where(magnitude_spectrum != 1)
    intense_points = np.where(magnitude_spectrum == 2)

    a = float(len(all_points) * len(all_points[0]))
    b = float(len(intense_points) * len(intense_points[0]))

    return b / a


pattern_regonition('patterns/pattern_47.jpg')
pattern_regonition('non_pattern/non_pattern_11.jpg')

"""print "Pattern images:"
print 'patterns/pattern_1.png: ', pattern_regonition('patterns/pattern_1.jpg')
print 'patterns/pattern_0.jpg: ', pattern_regonition('patterns/pattern_2.jpg')
print 'patterns/pattern_3.jpeg: ', pattern_regonition('patterns/pattern_3.jpg')
print 'patterns/pattern_4.jpg: ', pattern_regonition('patterns/pattern_4.jpg')
print 'patterns/pattern_5.png: ', pattern_regonition('patterns/pattern_5.jpg')
print 'patterns/pattern_6.png: ',pattern_regonition('patterns/pattern_6.jpg')
print 'patterns/pattern_7.png: ',pattern_regonition('patterns/pattern_7.jpg')
print 'patterns/pattern_8.png: ',pattern_regonition('patterns/pattern_8.jpg')
print 'patterns/pattern_9.png: ',pattern_regonition('patterns/pattern_9.jpg')
print 'patterns/pattern_10.png: ',pattern_regonition('patterns/pattern_10.jpg')

print "Non pattern images:"
print 'non_pattern/non_pattern_1.jpg: ', pattern_regonition('non_pattern/non_pattern_1.jpg')
print 'non_pattern/non_pattern_2.jpg: ', pattern_regonition('non_pattern/non_pattern_2.jpg')
print 'non_pattern/non_pattern_3.jpg: ', pattern_regonition('non_pattern/non_pattern_3.jpg')
print 'non_pattern/non_pattern_4.jpg: ', pattern_regonition('non_pattern/non_pattern_4.jpg')
print 'non_pattern/non_pattern_5.jpg: ', pattern_regonition('non_pattern/non_pattern_5.jpg')
print 'non_pattern/non_pattern_6.jpg: ', pattern_regonition('non_pattern/non_pattern_6.jpg')
print 'non_pattern/non_pattern_7.jpg: ', pattern_regonition('non_pattern/non_pattern_7.jpg')
print 'non_pattern/non_pattern_8.jpg: ', pattern_regonition('non_pattern/non_pattern_8.jpg')
print 'non_pattern/non_pattern_9.jpg: ', pattern_regonition('non_pattern/non_pattern_9.jpg')
print 'non_pattern/non_pattern_10.jpg: ', pattern_regonition('non_pattern/non_pattern_10.jpg')

print "Random pattern like"
print 'random/random_1.jpg: ', pattern_regonition('random/random_1.jpg')
print 'random/random_2.jpg: ', pattern_regonition('random/random_2.jpg')
print 'random/random_3.jpg: ', pattern_regonition('random/random_3.jpg')
print 'random/random_4.jpg: ', pattern_regonition('random/random_4.jpg')"""
