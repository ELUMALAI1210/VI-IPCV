import cv2
import numpy as np

def apply_threshold(image):
    """
    Apply Binary Thresholding.
    """
    _, thresholded = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresholded

def apply_morphology(image):
    """
    Apply Morphological Operations: Opening (noise removal), Closing (fill holes), and Dilation.
    """
    kernel = np.ones((3, 3), np.uint8)
    
    # Opening to remove noise
    opened = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    
    # Closing to fill small holes inside the foreground objects
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
    
    # Dilation to make features more prominent
    dilated = cv2.dilate(closed, kernel, iterations=1)
    
    return dilated
