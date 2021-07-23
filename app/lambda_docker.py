import os
import time

from flask import Flask, jsonify, request

from .common import load_from_s3, load_from_disk

app = Flask(__name__)

MODEL_SOURCE = os.environ.get('MODEL_SOURCE')
if MODEL_SOURCE  == 'S3':
    print("Loading model from S3")
    MODEL = load_from_s3()
elif MODEL_SOURCE == 'DISK':
    print("Loading model from disk")
    MODEL = load_from_disk()
else:
    raise ValueError(f"Invalid value for MODEL_SOURCE: {MODEL_SOURCE}")

features = [
    'age', 
    'fnlwgt', 
    'education_num', 
    'capital_gain', 
    'capital_loss', 
    'hours_per_week'
]

@app.route("/")
def serve():
    return jsonify(success=True)

@app.route("/predict", methods=["POST"])
def predict():
    request_payload = request.json
    payload = [request_payload[feature] for feature in features]
    proba = MODEL.predict_proba([payload])[0][1] 
    return {
        'prediction': '>$50K' if proba >= 0.5 else '<=$50K',
        'probability': proba
    }

@app.route("/time")
def get_current_time():
    return {"time": f"Time is {round(time.time())}"}

@app.route("/timev2", methods=["POST"])
def get_current_time_post():
    return {"time": f"Time is {round(time.time())}"}
