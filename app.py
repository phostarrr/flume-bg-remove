from flask import Flask, render_template
import requests 
import os


app = Flask(__name__)

API_KEY = "2ycZNwEiuHKr9AxyfBUvhZDf"  # <-- PASTE YOUR ACTUAL API KEY HERE!
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':    
    app.run(debug=True)