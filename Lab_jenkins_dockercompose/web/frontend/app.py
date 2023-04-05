import os
from flask import Flask, render_template
import cv2
import requests
import uvicorn
import base64
from fastapi import FastAPI
from pydantic import BaseModel
import matplotlib.pyplot as plt
import numpy as np
import cv2
import json

app = FastAPI()

app = Flask(__name__,template_folder="")
def encode_image(image):
    _, encoded_image = cv2.imencode(".jpg", image)
    return "data:image/jpeg;base64," + base64.b64encode(encoded_image).decode()

# decode base64 string to image
def decode_image(image_string):
    encoded_data = image_string.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

url = "http://52.23.238.240:8088"

@app.route('/')
def template():
    image_file = 'pang.jpg'
    image_file2 = 'kai.jpg'
    image_file3 = 'mamon.jpg'
    

    # Load the image
    image        = cv2.imread(image_file)
    image_string = encode_image(image)
    image2        = cv2.imread(image_file2)
    image_string2 = encode_image(image2)
    image3        = cv2.imread(image_file3)
    image_string3 = encode_image(image3)
    payload = {
        "image": image_string,
        "name": "pang",
        "surname": "rosjana",
        "numbers": [1, 2, 3, 4, 5]
    }
    response = requests.post(f"{url}/process-image", json=payload)

    data = json.loads(response.content)

    processed_image_string = data["processed_image"]
    processed_image        = decode_image(processed_image_string)

    return render_template("index.html", mycontent=image_string, mycontent2=image_string2, mycontent3=image_string3, name=data)    

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="8081")