import logging
from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename
from utils.web_scraper import scrape_dress_images
from utils.image_processing import process_user_image
from utils.fitting import perform_dress_fitting

# Initialize Flask App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/images/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        logging.error("No file part in the request.")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        logging.error("No selected file.")
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        logging.info(f"Attempting to save the file: {filename} to {filepath}")
        
        try:
            file.save(filepath)
            logging.info(f"File saved successfully at {filepath}")

            # Process the uploaded user image
            user_data = process_user_image(filepath)
            return jsonify({'message': 'Image uploaded successfully', 'user_data': user_data}), 200
        except Exception as e:
            logging.error(f"Error saving file: {e}")
            return jsonify({'error': f'Failed to save file: {e}'}), 500
    else:
        logging.error(f"Invalid file type: {file.filename}")
        return jsonify({'error': 'Invalid file type'}), 400

# Other routes...

if __name__ == '__main__':
    app.run(debug=True)
