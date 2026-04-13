"""
app.py — Flask application with 5 REST API endpoints.
Run: python app.py
"""

import csv
import io
from flask import Flask, request, jsonify, send_file, render_template

from database import (
    get_connection, create_tables, seed_categories,
    insert_upload, insert_transactions,
    get_all_transactions, get_summary,
    get_all_categories, get_transactions_for_download,
)
from csv_parser import parse_csv
from categorizer import categorize_rows

app = Flask(__name__)

# ── Initialise DB on startup ─────────────────────────────────────────────────
with app.app_context():
    conn = get_connection()
    create_tables(conn)
    seed_categories(conn)
    conn.close()


# ── Page routes ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/transactions")
def transactions_page():
    return render_template("transactions.html")


@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")


# ── API: POST /api/upload ────────────────────────────────────────────────────

@app.route("/api/upload", methods=["POST"])
def api_upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    if not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "Only CSV files are supported"}), 400

    try:
        raw_bytes = file.read()
        rows = parse_csv(raw_bytes)
        rows = categorize_rows(rows)
    except ValueError as e:
        return jsonify({"error": str(e)}), 422

    conn = get_connection()
    upload_id = insert_upload(conn, file.filename)
    count = insert_transactions(conn, rows, upload_id)
    conn.close()

    return jsonify({
        "status": "success",
        "upload_id": upload_id,
        "rows": count,
    }), 201


# ── API: GET /api/transactions ───────────────────────────────────────────────

@app.route("/api/transactions", methods=["GET"])
def api_transactions():
    category = request.args.get("category")
    conn = get_connection()
    rows = get_all_transactions(conn, category=category)
    conn.close()
    data = [
        {
            "id": r["id"],
            "date": r["date"],
            "description": r["description"],
            "amount": r["amount"],
            "type": r["type"],
            "category": r["category"],
            "upload_id": r["upload_id"],
        }
        for r in rows
    ]
    return jsonify(data)


# ── API: GET /api/summary ────────────────────────────────────────────────────

@app.route("/api/summary", methods=["GET"])
def api_summary():
    conn = get_connection()
    summary = get_summary(conn)
    conn.close()
    return jsonify(summary)


# ── API: GET /api/download ───────────────────────────────────────────────────

@app.route("/api/download", methods=["GET"])
def api_download():
    conn = get_connection()
    rows = get_transactions_for_download(conn)
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Description", "Amount", "Type", "Category"])
    for r in rows:
        writer.writerow([r["date"], r["description"], r["amount"], r["type"], r["category"]])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="categorized_transactions.csv",
    )


# ── API: GET /api/categories ─────────────────────────────────────────────────

@app.route("/api/categories", methods=["GET"])
def api_categories():
    conn = get_connection()
    cats = get_all_categories(conn)
    conn.close()
    return jsonify(cats)


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5000)
