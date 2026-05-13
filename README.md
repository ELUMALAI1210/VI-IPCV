# Pothole and Road Crack Detection System

A computer vision-based system to detect potholes and road cracks using image processing techniques.

## Features
- **Image Upload Mode**: Select an image from your computer to detect defects.
- **Real-Time Camera Mode**: Use your webcam for live pothole and crack detection.
- **Traditional CV Pipeline**: Uses Canny edge detection, thresholding, and morphological operations.
- **Classification**: Distinguishes between potholes (large, circular) and cracks (thin, elongated).

## Project Structure
- `preprocessing/`: Image resizing, grayscale conversion, and blurring.
- `detection/`: Core algorithms for edge detection, morphology, and defect classification.
- `app.py`: Main application script with GUI file dialog and camera support.
- `test_detection.py`: Utility to verify system with synthetic data.

## Installation
1. Install Python 3.x
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the main application:
```bash
python app.py
```

### Modes:
1. **Option 1**: Opens a file dialog to select an image. Displays intermediate steps and final detection results.
2. **Option 2**: Opens the webcam. Press **'q'** to exit.

## Algorithm Details
1. **Preprocessing**: Image is resized to 640x480, converted to grayscale, and smoothed using Gaussian Blur.
2. **Edge Detection**: Canny algorithm identifies potential defect boundaries.
3. **Thresholding**: Binary thresholding segments dark regions (defects) from the road surface.
4. **Morphology**: Closing and Dilation operations bridge gaps in edges and fill small holes.
5. **Feature Extraction**: Contours are detected and filtered by area.
6. **Classification**:
   - **Pothole**: Area > 2000 and aspect ratio between 0.5 and 2.0.
   - **Crack**: Area > 100 or extreme aspect ratio.
