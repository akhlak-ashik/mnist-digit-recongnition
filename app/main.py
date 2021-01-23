import os
from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow import keras
import cv2
import base64

# App and model initializer
app = Flask(__name__)
title = 'Number Recognizer'

# Loading prebuilt AI
model = keras.models.load_model('app/ai.h5')

# GET method
@app.route('/')
def home():
    return render_template('home.html', title=title)


# POST method
@app.route('/', methods=['POST'])
def result():
    print('Post request recieved')
    file_str = request.files['file'].read()
    file_np = np.fromstring(file_str, np.uint8)
    print(f'File recieved : {file_np.shape}')

    file_np = cv2.resize(file_np,(28,28))
    file_np = np.expand_dims(file_np, axis=0)

    try:
        prediction = np.argmax(model.predict(file_np))
        print(f"Prediction : {str(prediction)}")
        response = jsonify(response = str(prediction),status = 200)
    except Exception as e:
        response = jsonify(response = str(e),status = 400)

    return response

@app.route('/canvas', methods=['POST'])
def canvas():
    encoded_data = request.form['canvasimg'].split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite('28x28.jpg', img)
    img = img.transpose(2,0,1).reshape(3,-1)
    img = cv2.resize(img,(28,28))
    # cv2.imwrite('28x28.jpg', img)
    img = np.expand_dims(img, axis=0)

    try:
        prediction = np.argmax(model.predict(img))
        print(f"Prediction : {str(prediction)}")
        response = jsonify(response = str(prediction),status = 200)
    except Exception as e:
        response = jsonify(response = str(e),status = 400)

    return response