import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import tensorflow as tf
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'image_restoration_model.h5'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


try:
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {str(e)}")
    model = None


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if model is None:
        return jsonify({'error': 'Model not loaded. Please check server logs.'}), 500

    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']

    # Validation checks
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    if len(file.read()) > MAX_FILE_SIZE:
        return jsonify({'error': 'File too large (max 10MB)'}), 400
    file.seek(0)
    try:

        img = Image.open(file.stream).convert('RGB')
        original_size = img.size
        img = img.resize((256, 256))

        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        processed_array = model.predict(img_array)
        processed_array = np.clip(processed_array, 0, 1)


        processed_img = Image.fromarray((processed_array[0] * 255).astype(np.uint8))
        processed_img = processed_img.resize(original_size)  # Restore original dimensions


        buffered = BytesIO()
        processed_img.save(buffered, format="JPEG", quality=90)
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return jsonify({
            'status': 'success',
            'repaired_image': img_str,
            'original_size': original_size
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': f'Processing failed: {str(e)}'
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)