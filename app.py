from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Allow requests from any origin (needed for frontend on Netlify)

# Helper function to connect to DB
def db():
    return sqlite3.connect("sales.db", check_same_thread=False)

# ADD NEW ENTRY
@app.route("/add", methods=["POST"])
def add():
    d = request.json
    con = db()
    cur = con.cursor()

    cur.execute("""
    INSERT INTO sales(name, desc, date, time, price, trip, diesel, total)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        d.get("name", ""),
        d.get("desc", ""),
        d.get("date", ""),
        d.get("time", ""),
        d.get("price", 0),
        d.get("trip", 1),
        d.get("diesel", 0),
        d.get("total", 0)
    ))

    con.commit()
    con.close()
    return jsonify({"status": "saved"})

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

# UPDATE EXISTING ENTRY
@app.route("/update/<int:item_id>", methods=["PUT"])
def update(item_id):
    d = request.json
    con = db()
    cur = con.cursor()

    cur.execute("""
    UPDATE sales
    SET name = ?, desc = ?, date = ?, price = ?, trip = ?, diesel = ?, total = ?
    WHERE id = ?
    """, (
        d.get("name", ""),
        d.get("desc", ""),
        d.get("date", ""),
        d.get("price", 0),
        d.get("trip", 1),
        d.get("diesel", 0),
        d.get("total", 0),
        item_id
    ))

    con.commit()
    con.close()
    return jsonify({"status": "updated"})

# DELETE AN ENTRY (optional but recommended)
@app.route("/delete/<int:item_id>", methods=["DELETE"])
def delete(item_id):
    con = db()
    cur = con.cursor()
    cur.execute("DELETE FROM sales WHERE id = ?", (item_id,))
    con.commit()
    con.close()
    return jsonify({"status": "deleted"})

# SEARCH BY DATE
@app.route("/search", methods=["GET"])
def search():
    query_date = request.args.get("date")
    if not query_date:
        return jsonify({"error": "date query parameter is required"}), 400

    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM sales WHERE date = ? ORDER BY time DESC", (query_date,))
    cols = [d[0] for d in cur.description]
    result = [dict(zip(cols, r)) for r in cur.fetchall()]
    con.close()
    return jsonify(result)

# RUN SERVER
if __name__ == "__main__":
    # For Render / production, use host 0.0.0.0 and port from env
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
