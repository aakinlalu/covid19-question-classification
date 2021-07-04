import os

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASS = os.getenv("POSTGRES_PASS")
POSTGRES_HOST = "losthost"
POSTGRES_PORT = 5438
POSTGRES_NAME = "postgres"

MODEL_URL_PATH = "s3://ml-artifact-store/model/3://ml-artifact-store/model/experiment_run_1_covid_classifier/model"
