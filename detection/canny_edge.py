import cv2

def apply_canny(image, low_threshold=50, high_threshold=150):
    """
    Apply Canny Edge Detection.
    """
    edges = cv2.Canny(image, low_threshold, high_threshold)
    return edges
