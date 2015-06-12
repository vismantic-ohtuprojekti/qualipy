import cv2
import numpy as np

def reduce_colors(image, colors):
    """
    Reduces colors of given image to given amount. Algorithm uses K-nearest neighbors
    method to do this. Given image must have colors meaning three channels.

    param image: image to process (must have three channels)
    param colors: how many colors the final image should have
    """
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
