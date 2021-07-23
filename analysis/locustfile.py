import logging
import time

from locust import HttpUser, task, between

class BasicUser(HttpUser):
    wait_time = between(3, 5)
    payload = {
            "age": 34, 
            "fnlwgt": 261799, 
            "education_num": 11, 
            "capital_gain": 0, 
            "capital_loss": 0, 
            "hours_per_week": 56
    }

    @task
    def ml_request(self):
        start = time.time()
        response = self.client.post("/predict", json=self.payload)
        end = time.time()
        logging.info(f"{1000*(end-start):0.2f}")
