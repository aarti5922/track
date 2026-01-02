import psycopg2
import os

con = psycopg2.connect(os.environ["DATABASE_URL"])
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS sales")

cur.execute("""
CREATE TABLE sales(
  id SERIAL PRIMARY KEY,
  name TEXT,
  "desc" TEXT,
  date TEXT,
  time TEXT,
  price FLOAT,
  trip INT,
  diesel INT,
  total FLOAT
)
""")

con.commit()
con.close()

print("PostgreSQL Database initialized successfully!")
