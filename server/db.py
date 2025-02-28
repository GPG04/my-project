import psycopg2 # type: ignore
import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")

try:
    db = psycopg2.connect(database_url)
    cursor = db.cursor()
    print("Success!!!")
except (Exception, psycopg2.DatabaseError) as error:
    print(error)