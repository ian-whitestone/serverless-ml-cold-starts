

## Setup
1. Make sure you have [poetry](https://python-poetry.org/docs/#installation), the [AWS CLI](https://aws.amazon.com/cli/) & [docker](https://docs.docker.com/get-docker/) installed on your system
2. Clone the repo and set your working directory to the root of the repository (i.e. `cd path/to/serverless-ml-deployments`)
3. Run `poetry install --no-root`


## Building the Docker image
1. Run `zappa save-python-settings-file lambda_docker_flask_ml -o zappa_settings.py` to generate & save the Python settings file required by Zappa
2. Build the Docker image with `docker build -t lambda-docker-flask-ml:latest .`
3. Create a new ECR repository by running `aws ecr create-repository --repository-name lambda-docker-flask-ml --image-scanning-configuration scanOnPush=true`
4. Authenticate your local machine so it can push images to your repostiroy by running `aws ecr get-login-password | docker login --username AWS --password-stdin <your_registry_id>.dkr.ecr.us-east-1.amazonaws.com`
5. Point your Docker image to your new repository `docker tag lambda-docker-flask-ml:latest <your_registry_id>.dkr.ecr.us-east-1.amazonaws.com/lambda-docker-flask-ml:latest`
6. And push it `docker push <your_registry_id>.dkr.ecr.us-east-1.amazonaws.com/lambda-docker-flask-ml:latest`

## Deploying with Zappa

Deploying the lambda function with your new Docker image can be accomplished by using the `zappa deploy` command and passing in the Docker image URI:

`zappa deploy lambda_docker_flask_ml -d <your_registry_id>.dkr.ecr.us-east-1.amazonaws.com/lambda-docker-flask:latest`


## Performance testing with locust

`locust -f analysis/locustfile.py --host https://okxxo17i90.execute-api.us-east-1.amazonaws.com/lambda_docker_flask_ml --users 100 --spawn-rate 100 --run-time 60s --csv DOCKER_DISK --csv-full-history --html --logfile DOCKER_DISK_locust_logs.txt`