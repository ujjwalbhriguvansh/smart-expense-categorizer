"""
categorizer.py - Rule-based keyword matching engine.
description -> UPPERCASE -> keyword dict lookup -> assign category
"""

KEYWORD_MAP = {
    "Salary / Income":     ["SALARY", "BONUS", "STIPEND", "INCOME", "PAYROLL"],
    "Food":                ["SWIGGY", "ZOMATO", "DOMINOS", "STARBUCKS",
                            "GROCERY STORE", "UBER EATS", "SWIGGY INSTAMART",
                            "FLIPKART GROCERY", "BIGBASKET", "BLINKIT",
                            "DUNZO", "CAFE", "RESTAURANT"],
    "Travel":              ["UBER TRIP", "OLA CAB", "OLA AUTO", "OLA BIKE",
                            "RAPIDO", "REDBUS", "IRCTC", "MAKEMYTRIP", "GOIBIBO"],
    "Shopping":            ["AMAZON INDIA", "FLIPKART", "MYNTRA", "MEESHO",
                            "NYKAA", "AJIO", "SNAPDEAL", "BOOK STORE"],
    "Bills & Utilities":   ["ELECTRICITY BILL", "WATER BILL", "MOBILE RECHARGE",
                            "BROADBAND", "INTERNET BILL", "GAS BILL",
                            "POSTPAID", "AMAZON PAY BILL"],
    "Entertainment":       ["NETFLIX", "SPOTIFY", "BOOKMYSHOW", "AMAZON PRIME",
                            "HOTSTAR", "YOUTUBE PREMIUM", "DISNEY"],
    "Healthcare":          ["APOLLO PHARMACY", "MEDPLUS", "HOSPITAL", "LAB TEST",
                            "DIAGNOSTIC", "CLINIC", "PHARMEASY", "NETMEDS",
                            "MEDICAL STORE"],
    "Insurance":           ["LIC INSURANCE", "HDFC LIFE", "BAJAJ ALLIANZ",
                            "STAR HEALTH", "INSURANCE PREMIUM"],
    "Savings / Transfers": ["TRANSFER TO SAVINGS", "TRANSFER FROM FRIEND",
                            "TRANSFER FROM CLIENT", "NEFT TO", "IMPS TO",
                            "UPI TRANSFER", "TRANSFER TO WALLET"],
    "Investments / Interest": ["INTEREST CREDIT", "INTEREST CREDIT FD",
                               "MUTUAL FUND", "STOCKS"],
    "Education":           ["UDEMY", "COURSERA", "COLLEGE FEE", "SCHOOL FEE",
                            "TUITION", "BYJU", "UNACADEMY"],
    "Rent":                ["RENT PAYMENT", "HOUSE RENT", "PG PAYMENT", "RENT TRANSFER"],
    "Gym":                 ["GYM MEMBERSHIP"],
}

def categorize(description):
    upper = description.upper()
    for category, keywords in KEYWORD_MAP.items():
        for kw in keywords:
            if kw in upper:
                return category
    return "Other"

def categorize_rows(rows):
    for row in rows:
        row["category"] = categorize(row.get("description", ""))
    return rows