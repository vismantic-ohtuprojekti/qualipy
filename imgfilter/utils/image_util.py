import cv2


def sharpen(image):
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    return cv2.addWeighted(image, 1.5, blur, -0.5, 0)


def to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
