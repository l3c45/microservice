import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to an existing database
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

cur = conn.cursor()

def getUser(username):
  cur=None
  
  try:
    cur = conn.cursor()
    cur.execute(
        'SELECT email, password FROM "user" WHERE email=%s', (username)
    )
  
    row=cur.fetchone()
    print(row)
    return{
      "email":row[0],
      "password":row[1]
    }
  except Exception as e:
    None
  finally:
    if(cur):
      cur.close()
    conn.close()