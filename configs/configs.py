import os

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASS = os.getenv("POSTGRES_PASS")
POSTGRES_HOST = "losthost"
POSTGRES_PORT = 5438
POSTGRES_NAME = "postgres"

DATABASE_URL = os.getenv("DATABASE_URL")

DATABASE_URLs = f"postgresql://localhost:5438/postgres"
