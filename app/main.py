import os
from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow import keras
import cv2

# App and model initializer
app = Flask(__name__)
title = 'Number Recognizer'

# GET method
@app.route('/')
def home():
    return render_template('home.html', title=title)


# POST method
@app.route('/', methods=['POST'])
def result():
    file_str = request.files['file'].read()
    file_np = np.fromstring(file_str, np.uint8)
    file_np = cv2.resize(file_np,(28,28))
    file_np = np.expand_dims(file_np, axis=0)

    try:
    	model = keras.models.load_model('app/ai.h5')
    	prediction = np.argmax(model.predict(file_np))
    	response = jsonify(response = str(prediction),status = 200)
    except Exception as e:
    	response = jsonify(response = str(e),status = 400)

    return response