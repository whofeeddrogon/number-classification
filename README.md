# Number Classification Web Application
#### Video Demo:  <URL HERE>

## Overview

This web application is designed to classify handwritten digits using a machine learning model. Users can draw a digit on a canvas, which is then sent to the server for classification. The server processes the image, feeds it into a pre-trained ONNX model, and returns the predicted digit.

## Directory Structure

- `/static/`
  - `styles.css` (CSS styles for the web app)
- `/templates/`
  - `index.html` (HTML template for the main page)
- `/data/`
  - `mnist-12.onnx` (The pre-trained ONNX model for digit classification)
- `app.py` (The Flask application)

## Frontend

### HTML (`/templates/index.html`)

- The HTML file defines the structure of the web application's user interface.
- It includes a drawing canvas where users can draw a digit.
- Two buttons are provided: "Send" to submit the drawing for classification and "Clear board" to reset the canvas.
- The prediction result is displayed in a paragraph with the id `prediction`.

### CSS (`/static/styles.css`)

- This file contains the styling for the HTML template, including the canvas and button aesthetics.

### JavaScript (Embedded in `/templates/index.html`)

- Handles the drawing functionality on the canvas.
- Captures the canvas content and sends it to the server for classification upon clicking the "Send" button.
- Provides functionality to clear the canvas with the "Clear board" button.

## Backend (`app.py`)

### Flask Application

- The Flask app serves the HTML template and handles requests to the root endpoint (`/`).
- The `/classify` endpoint accepts POST requests with base64 encoded image data, processes it, and returns the classification result.

### Image Preprocessing

- The `preprocess_image` function prepares the image for the model by ensuring it's in the correct format and dimensions.
- It converts the image to grayscale, resizes it to 28x28 pixels, inverts color, and normalizes the pixel values.

### ONNX Model Loading and Inference

- The ONNX model is loaded at startup.
- The `/classify` endpoint uses the `onnxruntime` to run inference on the preprocessed image and returns the predicted digit.

### Exception Handling

- The classification endpoint includes error handling to return a server error response in case of exceptions during the image processing or classification process.

## Running the Application

- The application can be started by running `app.py` which will host the server on `localhost` and default port `5000`.
- The `debug` mode is turned on for development purposes, allowing for live updates without restarting the server.

## Usage

1. Start the Flask server by running `app.py`.
2. Open a web browser and navigate to `http://localhost:5000/`.
3. Use the mouse to draw a digit on the canvas.
4. Click the "Send" button to get the classification result.
5. The predicted digit will be displayed below the canvas.
6. Use the "Clear board" button to reset the canvas and draw a new digit.

**Note:** This documentation assumes the server and model are properly set up and that the necessary libraries are installed. Users should have Flask and onnxruntime installed in their Python environment to run the application.