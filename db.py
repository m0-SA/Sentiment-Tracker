import os

import psycopg
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")


def get_connection():

    print("Establishing Connection...")
    return psycopg.connect(db_url)
