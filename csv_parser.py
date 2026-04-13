"""
csv_parser.py - Reads a bank CSV and returns clean row dicts.
Expected CSV columns (case-insensitive): date, description, amount, type
"""
import csv
import io

REQUIRED_COLS = {"date", "description", "amount", "type"}

def parse_csv(file_bytes):
    text = file_bytes.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))

    if reader.fieldnames is None:
        raise ValueError("CSV file is empty or has no header row.")

    fieldnames_lower = [f.strip().lower() for f in reader.fieldnames]
    missing = REQUIRED_COLS - set(fieldnames_lower)
    if missing:
        raise ValueError("CSV missing required columns: " + ", ".join(missing))

    rows = []
    for i, raw in enumerate(reader, start=2):
        row = {k.strip().lower(): v.strip() for k, v in raw.items() if k}

        if not row["date"]:
            raise ValueError("Row " + str(i) + ": date is empty.")
        if not row["description"]:
            raise ValueError("Row " + str(i) + ": description is empty.")

        try:
            amount = float(row["amount"])
        except ValueError:
            raise ValueError("Row " + str(i) + ": amount is not a valid number.")

        tx_type = row["type"].lower()
        if tx_type not in ("debit", "credit"):
            tx_type = "credit" if amount >= 0 else "debit"

        rows.append({
            "date":        row["date"],
            "description": row["description"],
            "amount":      amount,
            "type":        tx_type,
        })
    return rows