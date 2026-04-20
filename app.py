from flask import Flask, render_template
import requests 
import os


app = Flask(__name__)

API_KEY = "2ycZNwEiuHKr9AxyfBUvhZDf"  # <-- PASTE YOUR ACTUAL API KEY HERE!
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

def remove_background(input_path, output_path):
    """Call the remove.bg API to process the image"""
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(input_path, 'rb')},
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
    
@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':    
    app.run(debug=True)