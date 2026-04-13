"""
csv_parser.py — Reads a bank CSV and returns clean row dicts.
Expected CSV columns (case-insensitive): date, description, amount, type
"""

import csv
import io


REQUIRED_COLS = {"date", "description", "amount", "type"}


def parse_csv(file_bytes: bytes) -> list[dict]:
    """
    Parse CSV bytes into a list of row dicts.
    Raises ValueError if required columns are missing.
    """
    text = file_bytes.decode("utf-8-sig")  # handles BOM from Excel exports
    reader = csv.DictReader(io.StringIO(text))

    # Normalise header names to lowercase
    if reader.fieldnames is None:
        raise ValueError("CSV file is empty or has no header row.")

    fieldnames_lower = [f.strip().lower() for f in reader.fieldnames]
    missing = REQUIRED_COLS - set(fieldnames_lower)
    if missing:
        raise ValueError(f"CSV missing required columns: {', '.join(missing)}")

    rows = []
    for i, raw in enumerate(reader, start=2):  # row 1 is header
        row = {k.strip().lower(): v.strip() for k, v in raw.items() if k}
        try:
            amount = float(row["amount"])
        except ValueError:
            raise ValueError(f"Row {i}: amount '{row['amount']}' is not a valid number.")

        tx_type = row["type"].lower()
        if tx_type not in ("debit", "credit"):
            # Auto-detect from sign if type value is wrong
            tx_type = "credit" if amount >= 0 else "debit"

        rows.append({
            "date":        row["date"],
            "description": row["description"],
            "amount":      amount,
            "type":        tx_type,
        })

    return rows
