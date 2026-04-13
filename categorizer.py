"""
categorizer.py — Rule-based keyword matching engine.
description → UPPERCASE → keyword dict lookup → assign category
"""

KEYWORD_MAP: dict[str, list[str]] = {
    "Salary / Income":    ["SALARY", "BONUS", "STIPEND", "INCOME", "PAYROLL"],
    "Food":               ["SWIGGY", "ZOMATO", "DOMINOS", "STARBUCKS", "GROCERY STORE",
                           "BIGBASKET", "BLINKIT", "DUNZO", "CAFE", "RESTAURANT"],
    "Travel":             ["UBER TRIP", "OLA CAB", "OLA AUTO", "OLA BIKE",
                           "RAPIDO", "REDBUS", "IRCTC", "MAKEMYTRIP", "GOIBIBO"],
    "Shopping":           ["AMAZON INDIA", "FLIPKART", "MYNTRA", "MEESHO",
                           "NYKAA", "AJIO", "SNAPDEAL"],
    "Bills & Utilities":  ["ELECTRICITY BILL", "WATER BILL", "MOBILE RECHARGE",
                           "BROADBAND", "INTERNET BILL", "GAS BILL", "POSTPAID"],
    "Entertainment":      ["NETFLIX", "SPOTIFY", "BOOKMYSHOW", "AMAZON PRIME",
                           "HOTSTAR", "YOUTUBE PREMIUM", "DISNEY"],
    "Healthcare":         ["APOLLO PHARMACY", "MEDPLUS", "HOSPITAL", "LAB TEST",
                           "DIAGNOSTIC", "CLINIC", "PHARMEASY", "NETMEDS"],
    "Insurance":          ["LIC INSURANCE", "HDFC LIFE", "BAJAJ ALLIANZ",
                           "STAR HEALTH", "INSURANCE PREMIUM"],
    "Savings / Transfers":["TRANSFER TO SAVINGS", "TRANSFER FROM FRIEND",
                           "TRANSFER FROM CLIENT", "NEFT TO", "IMPS TO", "UPI TRANSFER"],
    "Education":          ["UDEMY", "COURSERA", "COLLEGE FEE", "SCHOOL FEE",
                           "TUITION", "BYJU", "UNACADEMY"],
    "Rent":               ["RENT PAYMENT", "HOUSE RENT", "PG PAYMENT", "RENT TRANSFER"],
}


def categorize(description: str) -> str:
    """Return the category for a transaction description."""
    upper = description.upper()
    for category, keywords in KEYWORD_MAP.items():
        for kw in keywords:
            if kw in upper:
                return category
    return "Other"


def categorize_rows(rows: list[dict]) -> list[dict]:
    """Add a 'category' key to each row dict in-place and return the list."""
    for row in rows:
        row["category"] = categorize(row.get("description", ""))
    return rows
