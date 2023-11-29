import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
print(os.environ.get("DB_HOST"))

# Connect to an existing database
conn = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
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