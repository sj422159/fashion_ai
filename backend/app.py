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
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the uploaded user image
        user_data = process_user_image(filepath)
        return jsonify({'message': 'Image uploaded successfully', 'user_data': user_data}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/scrape', methods=['POST'])
def scrape_images():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Scrape 360° dress images from the URL
    try:
        images = scrape_dress_images(url)
        return jsonify({'message': 'Images scraped successfully', 'images': images}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/fit', methods=['POST'])
def fit_dress():
    data = request.json
    user_image = data.get('user_image')
    dress_image = data.get('dress_image')
    if not user_image or not dress_image:
        return jsonify({'error': 'Both user image and dress image are required'}), 400

    # Perform dress fitting
    try:
        fitting_results = perform_dress_fitting(user_image, dress_image)
        return jsonify({'message': 'Fitting performed successfully', 'results': fitting_results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
