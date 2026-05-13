import cv2

def detect_defects(morph_image, original_image):
    """
    Detect contours and classify into Cracks and Potholes using shape analysis.
    """
    contours, _ = cv2.findContours(morph_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    pothole_count = 0
    crack_count = 0
    result_image = original_image.copy()
    
    import math

    for cnt in contours:
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        
        # Area filtering for noise reduction
        if area < 50:
            continue
            
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = max(w, h) / min(w, h) if min(w, h) > 0 else 0
        
        # Circularity = (4 * PI * Area) / Perimeter^2
        circularity = (4 * math.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
        
        # Solidity = Area / Convex Hull Area
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        solidity = float(area) / hull_area if hull_area > 0 else 0
        
        # Classification logic
        # Potholes: High circularity, high solidity, moderate area, low aspect ratio
        # Cracks: Low circularity, low solidity (sometimes), thin (high aspect ratio)
        
        is_pothole = (area > 500 and circularity > 0.3 and aspect_ratio < 3.0) or (area > 1500 and circularity > 0.2)
        
        if is_pothole:
            label = "Pothole"
            color = (0, 0, 255) # Red
            pothole_count += 1
        elif area > 50:
            # For cracks, we look for elongated shapes (high aspect ratio) or very low circularity
            if aspect_ratio > 2.5 or circularity < 0.2:
                label = "Crack"
                color = (0, 255, 0) # Green
                crack_count += 1
            else:
                continue
        else:
            continue
            
        # Draw bounding box and label
        cv2.rectangle(result_image, (x, y), (x + w, y + h), color, 2)
        cv2.putText(result_image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
    return result_image, pothole_count, crack_count
