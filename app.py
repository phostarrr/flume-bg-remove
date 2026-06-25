from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import requests 
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv


app = Flask(__name__)

# --- CONFIGURATION ---
load_dotenv()

API_KEY = os.getenv('API_KEY') 
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_background(input_path, output_path):
    """Call the remove.bg API to process the image"""
    with open(input_path, 'rb') as f:
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': f},
            data={'size': 'auto'},
            headers={'X-Api-Key': API_KEY},
        )
    
    if response.status_code == requests.codes.ok:
        with open(output_path, 'wb') as out:
            out.write(response.content)
        return True
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return False

# --- ROUTES ---

@app.route('/')
def index():
    # Check if we have a processed image to show
    processed_image = request.args.get('processed_image')
    return render_template('index.html', processed_image=processed_image)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return redirect(request.url)

    # Save original
    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)

    # Prepare output path
    output_filename = f"no_bg_{filename}.png"
    output_path = os.path.join(app.config['RESULT_FOLDER'], output_filename)

    # Process via API
    if remove_background(input_path, output_path):

        return redirect(url_for('index', processed_image=output_filename))
    else:
        return "API Error. Check console.", 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename)

if __name__ == '__main__':    
    app.run(debug=True)