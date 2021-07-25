Code to support the [Serving machine learning models with AWS Lambda](https://ianwhitestone.work/serverless-ml-deployments) blog post.

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

I ran the following command to trigger a headless locust test:

`export PREFIX=DOCKER_DISK_v1 && locust -f locustfile.py --host <your_deployed_app_url> --users 100 --spawn-rate 20 --run-time 60s --csv "locust_logs/${PREFIX}" --csv-full-history --html "locust_logs/${PREFIX}_locust_report.html" --logfile "locust_logs/${PREFIX}_locust_logs.txt" --headless`

This outputs a bunch of files, including a log file `DOCKER_DISK_v1_locust_logs.txt` that looks like this:

```
[2021-07-24 15:37:19,239] Ians-MBP.local/INFO/locust.main: Run time limit set to 60 seconds
[2021-07-24 15:37:19,240] Ians-MBP.local/INFO/locust.main: Starting Locust 1.6.0
[2021-07-24 15:37:19,240] Ians-MBP.local/INFO/locust.runners: Spawning 100 users at the rate 20 users/s (0 users already running)...
[2021-07-24 15:37:24,568] Ians-MBP.local/INFO/locust.runners: All users spawned: BasicUser: 100 (100 total running)
[2021-07-24 15:37:25,745] Ians-MBP.local/INFO/root: 3799.82
[2021-07-24 15:37:26,095] Ians-MBP.local/INFO/root: 4666.09
[2021-07-24 15:37:27,096] Ians-MBP.local/INFO/root: 4245.08
[2021-07-24 15:37:27,397] Ians-MBP.local/INFO/root: 8106.02
[2021-07-24 15:37:27,398] Ians-MBP.local/INFO/root: 7946.65
[2021-07-24 15:37:27,399] Ians-MBP.local/INFO/root: 7841.94
[2021-07-24 15:37:27,502] Ians-MBP.local/INFO/root: 7734.79
[2021-07-24 15:37:27,798] Ians-MBP.local/INFO/root: 8453.01
...
...
[2021-07-24 15:38:18,536] Ians-MBP.local/INFO/root: 124.35
[2021-07-24 15:38:18,632] Ians-MBP.local/INFO/root: 62.76
[2021-07-24 15:38:18,649] Ians-MBP.local/INFO/root: 67.33
[2021-07-24 15:38:18,661] Ians-MBP.local/INFO/root: 92.54
[2021-07-24 15:38:18,667] Ians-MBP.local/INFO/locust.main: Time limit reached. Stopping Locust.
[2021-07-24 15:38:18,667] Ians-MBP.local/INFO/locust.runners: Stopping 100 users
[2021-07-24 15:38:18,682] Ians-MBP.local/INFO/locust.runners: 100 Users have been stopped, 0 still running
[2021-07-24 15:38:18,730] Ians-MBP.local/INFO/locust.main: Running teardowns...
[2021-07-24 15:38:18,731] Ians-MBP.local/INFO/locust.main: Shutting down (exit code 0), bye.
[2021-07-24 15:38:18,731] Ians-MBP.local/INFO/locust.main: Cleaning up runner...
```

This can then be consumed and parsed in Python to get the distribution of performance. See the code in [this notebook](https://github.com/ian-whitestone/serverless-ml-cold-starts/blob/master/analysis/lambda_performance.ipynb).