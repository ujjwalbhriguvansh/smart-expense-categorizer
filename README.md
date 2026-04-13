# 💰 Smart Expense Categorization & Personal Finance Insight Platform
**HCL Hackathon | Python + Flask + SQLite + HTML/JS**

---

## Project Structure

```
finance_app/
├── app.py                   # Flask app — 5 REST API endpoints + page routes
├── database.py              # SQLite setup, 3 tables, CRUD helpers
├── categorizer.py           # Rule-based keyword matching engine
├── csv_parser.py            # CSV parser — validates & cleans rows
├── requirements.txt
├── sample_transactions.csv  # Test data — 24 sample rows
├── static/
│   └── style.css
└── templates/
    ├── index.html           # Upload page
    ├── transactions.html    # Transactions view with category filter
    └── dashboard.html       # KPI cards + Pie + Bar charts
```

---

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app (DB is created automatically on first start)
python app.py

# 3. Open in browser
http://localhost:5000
```

---

## REST API Endpoints

| Method | Endpoint            | Description                               |
|--------|---------------------|-------------------------------------------|
| POST   | `/api/upload`       | Upload CSV → parse → categorise → store   |
| GET    | `/api/transactions` | All transactions (filter: `?category=X`)  |
| GET    | `/api/summary`      | Income, expenses, category totals         |
| GET    | `/api/download`     | Download categorised CSV                  |
| GET    | `/api/categories`   | List all 12 category names                |

---

## Categorisation Logic

Descriptions are converted to UPPERCASE and matched against keyword lists:

| Category          | Keywords (sample)                              |
|-------------------|------------------------------------------------|
| Salary / Income   | SALARY, BONUS                                  |
| Food              | SWIGGY, ZOMATO, DOMINOS, STARBUCKS             |
| Travel            | UBER TRIP, OLA CAB, OLA AUTO, IRCTC            |
| Shopping          | AMAZON INDIA, FLIPKART, MYNTRA                 |
| Bills & Utilities | ELECTRICITY BILL, WATER BILL, MOBILE RECHARGE  |
| Entertainment     | NETFLIX, SPOTIFY, BOOKMYSHOW, AMAZON PRIME     |
| Healthcare        | APOLLO PHARMACY, HOSPITAL, LAB TEST            |
| Insurance         | LIC INSURANCE                                  |
| Savings/Transfers | TRANSFER TO SAVINGS, TRANSFER FROM FRIEND      |
| Other             | (no match)                                     |

---

## Database Schema

```sql
categories  (id PK, name TEXT UNIQUE)
uploads     (id PK, filename TEXT, uploaded_at TIMESTAMP)
transactions(id PK, date, description, amount REAL,
             type CHECK(debit|credit),
             category FK→categories,
             upload_id FK→uploads)
```

---

## Tech Stack
- **Backend**: Python 3.11+, Flask 3.x
- **Database**: SQLite (via stdlib `sqlite3`)
- **Frontend**: Vanilla HTML/CSS/JS, Chart.js
- **No ORM** — raw SQL for clarity and performance
