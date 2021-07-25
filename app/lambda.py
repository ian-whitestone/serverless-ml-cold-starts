import pickle
import time

import boto3
from flask import Flask, jsonify, request

from .common import load_from_s3, load_from_disk

app = Flask(__name__)


print("Loading model from S3")
start = time.time()
model = load_from_s3()
end = time.time()
print(f"Model loaded in {(end-start):0.2f}!")

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
    proba = model.predict_proba([payload])[0][1] 
    return {
        'prediction': '>$50K' if proba >= 0.5 else '<=$50K',
        'probability': proba
    }
