import psycopg # type: ignore
import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")

try:
    db = psycopg.connect(database_url)
    cursor = db.cursor()
    print("Success!!!")
except (Exception, psycopg.DatabaseError) as error:
    print(error)