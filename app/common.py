import pickle

import boto3

def load_from_disk():
    with open('app/model.pkl', 'rb') as f_in:
        model = pickle.loads(f_in.read())
    return model

def load_from_s3():
    s3 = boto3.resource("s3")
    obj = s3.Object('serverless-ml-deployments', 'model.pkl')
    model_bytes = obj.get()["Body"].read()
    return pickle.loads(model_bytes)