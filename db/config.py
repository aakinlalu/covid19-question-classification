import os

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASS = os.getenv("POSTGRES_PASS")

DATABASE_URL = os.getenv("DATABASE_URL")

DATABASE_URLs = f"postgresql://localhost:5438/postgres"
