from dotenv import load_dotenv
import os
import psycopg2


load_dotenv()

db_url = os.getenv("PG_URL")
connection = psycopg2.connect(db_url)

cursor = connection.cursor()