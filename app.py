import cv2
import numpy as np
import os
import uuid
from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
from preprocessing.preprocess import preprocess_image
from detection.canny_edge import apply_canny
from detection.morphology import apply_threshold, apply_morphology
from detection.detect import detect_defects

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def process_frame(frame, session_id):
    """
    Complete pipeline for a single frame/image.
    Saves intermediate steps for visualization.
    """
    # 1. Preprocessing
    resized, blurred = preprocess_image(frame)
    
    # 2. Edge Detection
    edges = apply_canny(blurred)
    
    # 3. Thresholding
    thresh = apply_threshold(blurred)
    
    # 4. Combine Edge + Threshold
    combined = cv2.bitwise_or(edges, thresh)
    
    # 5. Morphological Operations
    morph = apply_morphology(combined)
    
    # 6. Detection and Classification
    result, p_count, c_count = detect_defects(morph, resized)
    
    # Save images to static/uploads
    def save_img(img, name):
        path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{name}.jpg")
        cv2.imwrite(path, img)
        return f"uploads/{session_id}_{name}.jpg"

    return {
        "original": save_img(resized, "original"),
        "edges": save_img(edges, "edges"),
        "threshold": save_img(thresh, "threshold"),
        "morph": save_img(morph, "morph"),
        "result": save_img(result, "result"),
        "p_count": p_count,
        "c_count": c_count
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        # We don't necessarily need to save the original file to disk if we process it immediately
        # but let's read it into memory
        file_bytes = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({"error": "Invalid image format"}), 400
            
        session_id = str(uuid.uuid4())[:8]
        results = process_frame(image, session_id)
        
        return jsonify(results)

if __name__ == '__main__':
    # Clean up uploads folder on start
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        if f.endswith(".jpg"):
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
            except:
                pass
                
    app.run(debug=True, host='0.0.0.0', port=5000)
