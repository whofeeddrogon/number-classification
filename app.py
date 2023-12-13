from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image, ImageOps
import io
import onnxruntime
import base64

app = Flask(__name__)

# Load the ONNX model
onnx_model_path = 'data/mnist-12.onnx'
sess = onnxruntime.InferenceSession(onnx_model_path)

def preprocess_image(image):
    # Check for transparency
    if image.mode == 'RGBA':
        # Create a white background image
        white_bg = Image.new('RGBA', image.size, (255, 255, 255, 255))
        # Paste the image onto the white background using the alpha channel as mask
        white_bg.paste(image, mask=image.split()[3])
        image = white_bg.convert('RGB')

    # Convert to grayscale
    image = image.convert('L')

    # Resize the image to match the model's expected sizing
    image = image.resize((28, 28))

    # Save the grayscale image for inspection
    image.save("/home/berkay/Desktop/grayscale_image.png")

    # Convert the image to a numpy array
    image_array = np.array(image)
    # Normalize the image
    image_array = 1 - (image_array.astype(np.float32) / 255.0)
    print(image_array)
    # Reshape the image to (1, 1, 28, 28)
    reshaped_image_array = image_array.reshape((1, 1, 28, 28))
    return reshaped_image_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    try:
        # Get the image data from the request
        img_data_base64 = request.json.get('data', '')

        # Decode the base64-encoded data part
        img_data_bytes = base64.b64decode(img_data_base64)

        # Convert the bytes to a PIL Image object directly
        image = Image.open(io.BytesIO(img_data_bytes))

        # Preprocess the image
        preprocessed_image = preprocess_image(image)

        # Make a prediction
        prediction = sess.run(None, {'Input3': preprocessed_image})

        # Get the predicted digit
        predicted_digit = np.argmax(prediction)

        return jsonify({'prediction': str(predicted_digit)})
    except Exception as e:
        print("Error:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)