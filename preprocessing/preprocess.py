import cv2

def preprocess_image(image, width=640, height=480):
    """
    Preprocess image: Resize, Grayscale conversion, Gaussian Blur.
    """
    # Resize
    resized = cv2.resize(image, (width, height))
    
    # Grayscale conversion
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    # Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    return resized, blurred
