import sqlite3

con = sqlite3.connect("sales.db")
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS sales")

cur.execute("""
CREATE TABLE sales(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  desc TEXT,
  date TEXT,
  time TEXT,
  price REAL,
  trip INTEGER,
  diesel INTEGER,
  total REAL
)
""")

con.commit()
con.close()

print("Database initialized successfully!")
