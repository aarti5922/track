from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# PostgreSQL connection
def db():
    return psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")

# ADD NEW ENTRY
@app.route("/add", methods=["POST"])
def add():
    try:
        d = request.json
        con = db()
        cur = con.cursor()

        cur.execute("""
        INSERT INTO sales(name, "desc", date, time, price, trip, diesel, total)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            d.get("name", ""),
            d.get("desc", ""),
            d.get("date", ""),
            d.get("time", ""),
            float(d.get("price", 0)),
            int(d.get("trip", 1)),
            float(d.get("diesel", 0)),
            float(d.get("total", 0))
        ))

        con.commit()
        con.close()
        return jsonify({"status": "saved"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET ALL ITEMS
@app.route("/items")
def items():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM sales ORDER BY date DESC, time DESC")
    cols = [d[0] for d in cur.description]
    result = [dict(zip(cols, r)) for r in cur.fetchall()]
    con.close()
    return jsonify(result)

# UPDATE
@app.route("/update/<int:item_id>", methods=["PUT"])
def update(item_id):
    try:
        d = request.json
        con = db()
        cur = con.cursor()

        cur.execute("""
        UPDATE sales
        SET name=%s, "desc"=%s, date=%s, price=%s, trip=%s, diesel=%s, total=%s
        WHERE id=%s
        """, (
            d.get("name", ""),
            d.get("desc", ""),
            d.get("date", ""),
            float(d.get("price", 0)),
            int(d.get("trip", 1)),
            float(d.get("diesel", 0)),
            float(d.get("total", 0)),
            item_id
        ))

        con.commit()
        con.close()
        return jsonify({"status": "updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE
@app.route("/delete/<int:item_id>", methods=["DELETE"])
def delete(item_id):
    con = db()
    cur = con.cursor()
    cur.execute("DELETE FROM sales WHERE id=%s", (item_id,))
    con.commit()
    con.close()
    return jsonify({"status": "deleted"})

# SEARCH
@app.route("/search")
def search():
    q = request.args.get("date")
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM sales WHERE date=%s ORDER BY time DESC", (q,))
    cols = [d[0] for d in cur.description]
    result = [dict(zip(cols, r)) for r in cur.fetchall()]
    con.close()
    return jsonify(result)

# RUN
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
