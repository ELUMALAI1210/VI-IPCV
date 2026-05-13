import cv2
import numpy as np
import os
from app import process_frame

def create_synthetic_road():
    # Create a gray "road" image
    img = np.full((480, 640, 3), 100, dtype=np.uint8)
    
    # Add some "cracks" (longer thin lines)
    cv2.line(img, (50, 50), (250, 100), (30, 30, 30), 2)
    cv2.line(img, (250, 100), (200, 300), (30, 30, 30), 2)
    
    # Add some "potholes" (ellipses/circles)
    cv2.circle(img, (400, 300), 40, (20, 20, 20), -1)
    cv2.ellipse(img, (200, 350), (60, 30), 0, 0, 360, (20, 20, 20), -1)
    
    # Add some noise correctly
    noise = np.random.normal(0, 5, img.shape)
    img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    
    return img

def test():
    print("Generating synthetic road image...")
    road_img = create_synthetic_road()
    cv2.imwrite("synthetic_road.jpg", road_img)
    
    print("Processing image...")
    outputs = process_frame(road_img)
    
    print(f"Detected Potholes: {outputs['p_count']}")
    print(f"Detected Cracks: {outputs['c_count']}")
    
    # Save results for verification
    cv2.imwrite("test_result.jpg", outputs["result"])
    cv2.imwrite("test_morph.jpg", outputs["morph"])
    
    print("Test images saved as 'synthetic_road.jpg', 'test_result.jpg', and 'test_morph.jpg'.")

if __name__ == "__main__":
    test()
