import cv2
import numpy as np
from matplotlib import pyplot as plt

def get_max_values(array_1D, count):
    max_values = np.array([])
    sorted = np.sort(array_1D)
    for i in range(array_1D.shape[0] - 1, array_1D.shape[0] - count - 1, -1):
        max_values = np.append(max_values, array_1D[i])
    return max_values


def avarage(array_1D):
    return np.sum(array_1D) / array_1D.shape[0]


def scale(value, min_value, max_value):
    return (value - min_value) / max_value

def remove_anomalies(array_1D, avarage, max_anonamaly, min_value, max_value):
    valid_values = np.array([])
    scaled_avarage = scale(avarage, min_value, max_value)

    for i in range(0, array_1D.shape[0]):
        value = scale(array_1D[i], min_value, max_value)
        if value < scaled_avarage + max_anonamaly and value > scaled_avarage - max_anonamaly:
            valid_values = np.append(valid_values, array_1D[i])

    return valid_values

def all_points_in_circle(array_2D, radii):
    all_points = 0.0
    center = np.array((array_2D.shape[0]/2.0, array_2D.shape[1]/2.0))

    for x in range(0, array_2D.shape[0]):
        for y in range(0, array_2D.shape[1]):
            distance_from_center = np.abs(np.linalg.norm(center - np.array((x,y))))

            if distance_from_center <= radii:
                all_points = all_points + 1.0

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
    image = cv2.imread(image_path)
    image = reduce_colors(image, 2)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    magnitude_spectrum = count_magnitude_spectrum(image)

    center = np.array((magnitude_spectrum.shape[0]/2.0, magnitude_spectrum.shape[1]/2.0))
    radii = (1.0/6.0) * np.linalg.norm(center)

    max_distance = 0.0
    all_distances = np.array([])
    dist_sum = 0.0

    non_zero_points = 0.0

    for x in range(0, magnitude_spectrum.shape[0]):
        for y in range(0, magnitude_spectrum.shape[1]):
            # Count distance from the center of the image
            distance_from_center = np.abs(np.linalg.norm(center - np.array((x,y))))

            # Make magnitude spectrum to contain only high values
            # and count all non zero points
            if magnitude_spectrum[x,y] > 0.70:
                magnitude_spectrum[x,y] = 1.0
                dist_sum = dist_sum + distance_from_center
                all_distances = np.append(all_distances, distance_from_center)
                non_zero_points = non_zero_points + 1
            else:
                magnitude_spectrum[x,y] = 0.0

            # Update max distance
            if distance_from_center > max_distance:
                max_distance = distance_from_center

    #print "max distance: ", max_distance, " for image: ", image_path
    avg_dist = dist_sum / non_zero_points
    all_distances = remove_anomalies(all_distances, avg_dist, 0.3, 0.0, max_distance)
    max_distance = avarage(get_max_values(all_distances, 20))
    all_points = all_points_in_circle(magnitude_spectrum, max_distance)
    return non_zero_points / all_points


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
print 'patterns/non_pattern_1.jpg: ', pattern_regonition('patterns/non_pattern_1.jpg')
print 'patterns/non_pattern_2.jpg: ', pattern_regonition('patterns/non_pattern_2.jpg')
print 'patterns/non_pattern_3.jpg: ', pattern_regonition('patterns/non_pattern_3.jpg')
print 'patterns/non_pattern_4.jpg: ', pattern_regonition('patterns/non_pattern_4.jpg')
print 'patterns/non_pattern_5.jpg: ', pattern_regonition('patterns/non_pattern_5.jpg')
print 'patterns/non_pattern_6.jpg: ', pattern_regonition('patterns/non_pattern_6.jpg')
print 'patterns/non_pattern_7.jpg: ', pattern_regonition('patterns/non_pattern_7.jpg')
print 'patterns/non_pattern_8.jpg: ', pattern_regonition('patterns/non_pattern_8.jpg')
print 'patterns/non_pattern_9.jpg: ', pattern_regonition('patterns/non_pattern_9.jpg')
print 'patterns/non_pattern_10.jpg: ', pattern_regonition('patterns/non_pattern_10.jpg')

print "Random pattern like"
print 'patterns/random_1.jpg: ', pattern_regonition('patterns/random_1.jpg')
print 'patterns/random_2.jpg: ', pattern_regonition('patterns/random_2.jpg')
print 'patterns/random_3.jpg: ', pattern_regonition('patterns/random_3.jpg')
print 'patterns/random_4.jpg: ', pattern_regonition('patterns/random_4.jpg')
