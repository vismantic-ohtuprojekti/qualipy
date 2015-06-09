import statistic_common

import cv2
import numpy as np
from matplotlib import pyplot as plt


def all_points_in_circle(array_2D, radii, image):
    all_points = 0.0
    center = np.array((array_2D.shape[0]/2.0, array_2D.shape[1]/2.0))

    for x in range(0, array_2D.shape[0]):
        for y in range(0, array_2D.shape[1]):
            distance_from_center = np.abs(np.linalg.norm(center - np.array((x,y))))

            if distance_from_center <= radii:
                all_points = all_points + 1.0
            else:
                array_2D[x,y] = 0.5

    plt.figure('Test')
    plt.subplot(121),plt.imshow(array_2D, cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(image, cmap = 'gray')
    plt.show()
    return all_points


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


def logaritmic_tarnsformation2D(array_2D):
    c = 1 / np.log(1 + np.abs(np.amax(array_2D)))
    return c * np.log(1 + np.abs(array_2D))


def count_magnitude_spectrum(image):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    return logaritmic_tarnsformation2D(fshift)


def pattern_regonition(image_path):
    # Reduce colors and turn into gray scale
    image = cv2.imread(image_path, 0)
    #image = reduce_colors(image, 2)
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Count magnitude spectrum
    magnitude_spectrum = count_magnitude_spectrum(image)

    # Center of the image
    center = np.array((magnitude_spectrum.shape[0]/2.0, magnitude_spectrum.shape[1]/2.0))

    all_distances = np.array([])
    non_zero_points = 0.0

    for x in range(0, magnitude_spectrum.shape[0]):
        for y in range(0, magnitude_spectrum.shape[1]):
            # Count distance from the center of the image
            distance_from_center = np.abs(np.linalg.norm(center - np.array((x,y))))

            # Make magnitude spectrum to contain only high values
            # and count all non zero points
            if magnitude_spectrum[x,y] > 0.80:
                magnitude_spectrum[x,y] = 1.0
                all_distances = np.append(all_distances, distance_from_center)
                non_zero_points = non_zero_points + 1
            else:
                magnitude_spectrum[x,y] = 0.0


    all_distances = statistic_common.remove_anomalies(all_distances, 0.2)
    max_distances = statistic_common.get_max_values(all_distances, 20)

    max_distance_avg = statistic_common.avarage(max_distances)
    all_points = all_points_in_circle(magnitude_spectrum, max_distance_avg, image)
    return non_zero_points / all_points


print 'patterns/Shadowgame.jpg: ', pattern_regonition('patterns/Shadowgame.jpg')
print "Pattern images:"
print 'patterns/pattern_0.jpg: ', pattern_regonition('patterns/pattern_0.jpg')
print 'patterns/pattern_1.png: ', pattern_regonition('patterns/pattern_1.png')
print 'patterns/pattern_3.jpeg: ', pattern_regonition('patterns/pattern_3.jpeg')
print 'patterns/pattern_4.jpg: ', pattern_regonition('patterns/pattern_4.jpg')
print 'patterns/pattern_5.png: ', pattern_regonition('patterns/pattern_5.png')
print 'patterns/pattern_6.png: ',pattern_regonition('patterns/pattern_6.jpeg')
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
print 'random/random_4.jpg: ', pattern_regonition('random/random_4.jpg')
