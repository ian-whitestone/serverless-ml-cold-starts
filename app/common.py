import os
import pickle

import boto3

MODEL_VERSION = os.environ['MODEL_VERSION']
MODEL_KEY = f'model_{MODEL_VERSION}.pkl'
def load_from_disk():
    print(f"Loading model {MODEL_KEY} from disk")
    with open(f'app/{MODEL_KEY}', 'rb') as f_in:
        model = pickle.loads(f_in.read())
    return model

def load_from_s3():
    print(f"Loading model {MODEL_KEY} from S3")
    s3 = boto3.resource("s3")
    obj = s3.Object('serverless-ml-deployments', MODEL_KEY)
    model_bytes = obj.get()["Body"].read()
    return pickle.loads(model_bytes)