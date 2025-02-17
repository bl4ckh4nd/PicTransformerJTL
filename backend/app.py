# backend/app.py
import os
import time
import logging
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
from PIL import Image
from flask_cors import CORS
from rembg import remove

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"]) # Enable CORS for Vite development server

INPUT_DIR = "input_images"
TEMP_DIR = "temp_images"
OUTPUT_DIR = "output_images"

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

PROCESSED_IMAGES = {}

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filepath = event.src_path
        if filepath.endswith(('.jpg', '.jpeg', '.png')):
            logger.info(f"New image detected: {filepath}")
            try:
                input_image = Image.open(filepath)
                output_image = remove(input_image)
                output_path = os.path.join(TEMP_DIR, os.path.basename(filepath).split('.')[0] + "_nobg.png")
                output_image.save(output_path)
                logger.info(f"Background removed from {filepath}, saved to {output_path}")
                self.process_images()
            except Exception as e:
                logger.error(f"Error removing background: {e}", exc_info=True)

    def process_images(self):
        image_files = [f for f in os.listdir(TEMP_DIR) if f.endswith(('.png'))]
        if len(image_files) >= 2:
            logger.info("Combining images...")
            try:
                image1_path = os.path.join(TEMP_DIR, image_files[0])
                image2_path = os.path.join(TEMP_DIR, image_files[1])
                image1 = Image.open(image1_path)
                image2 = Image.open(image2_path)
                width1, height1 = image1.size
                width2, height2 = image2.size
                new_width = width1 + width2 + 4
                new_height = max(height1, height2)
                new_image = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
                new_image.paste(image1, (0, 0))
                new_image.paste(image2, (width1 + 4, 0))
                output_path = os.path.join(OUTPUT_DIR, "combined_image.png")
                new_image.save(output_path)
                logger.info(f"Images combined and saved to {output_path}")
                # Clean up temporary files
                os.remove(image1_path)
                os.remove(image2_path)
            except Exception as e:
                logger.error(f"Error combining images: {e}", exc_info=True)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/images')
def get_images():
    try:
        image_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(('.png'))]
        return jsonify(image_files)
    except Exception as e:
        logger.error(f"Error getting images: {e}", exc_info=True)
        return jsonify({"message": "Error getting images"}), 500


@app.route('/images/<image_name>', methods=['DELETE'])
def delete_image(image_name):
    try:
        image_path = os.path.join(OUTPUT_DIR, image_name)
        if os.path.exists(image_path):
            os.remove(image_path)
            logger.info(f"Image deleted: {image_name}")
            return jsonify({"message": "Image deleted successfully"})
        else:
            return jsonify({"message": "Image not found"}), 404
    except Exception as e:
        logger.error(f"Error deleting image: {e}", exc_info=True)
        return jsonify({"message": "Error deleting image"}), 500

@app.route('/images/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"message": "No image part"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(INPUT_DIR, filename)
        file.save(filepath)
        logger.info(f"Image uploaded: {filepath}")
        return jsonify({"message": "File uploaded successfully"})
    return jsonify({"message": "File type not allowed"}), 400

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == '__main__':
    path = INPUT_DIR
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()