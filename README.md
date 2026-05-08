# 📊 Data Analysis Dashboar

An end-to-end data analysis project built with **Python**, **Pandas**, **Matplotlib**, **SQL (SQLite)**, and **Excel (openpyxl)**.

The project simulates a real-world e-commerce sales dataset (India-themed: cities, UPI payments, product categories) and runs a complete analytics pipeline — from raw data to automated charts and a formatted Excel report.

---

## 🚀 Features

| Feature | Details |
|---|---|
| **Data Generation** | 1,000+ synthetic records with intentional missing values & duplicates |
| **Data Cleaning** | Duplicate removal, null handling, dtype fixing, feature engineering |
| **SQL Analysis** | 6 business-insight queries via SQLite (no external DB needed) |
| **Visualizations** | 6 Matplotlib charts saved as PNG |
| **Excel Report** | Multi-sheet `.xlsx` with KPI summary, styled tables |

---

## 📁 Project Structure

```
data-analysis-dashboard/
│
├── main.py                    ← Run this to execute the full pipeline
│
├── src/
│   ├── generate_data.py       ← Creates synthetic sales dataset
│   ├── data_cleaning.py       ← Pandas cleaning & feature engineering
│   ├── sql_analysis.py        ← SQLite queries (monthly, category, city, etc.)
│   ├── visualizations.py      ← Matplotlib chart generation
│   └── report_generator.py    ← Automated Excel report (openpyxl)
│
├── data/
│   ├── raw/                   ← sales_data.csv (generated)
│   └── processed/             ← sales_clean.csv (after cleaning)
│
├── reports/                   ← Charts (PNG) + Excel report
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/data-analysis-dashboard.git
cd data-analysis-dashboard
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the full pipeline
```bash
python main.py
```

That's it! All outputs will be generated automatically.

---

## 📈 Generated Outputs

After running `main.py`, the `reports/` folder will contain:

| File | Description |
|---|---|
| `01_monthly_revenue.png` | Line chart — revenue trend across 12 months |
| `02_category_revenue.png` | Bar chart — revenue by product category |
| `03_top_cities.png` | Horizontal bar — top 10 cities by revenue |
| `04_payment_methods.png` | Pie chart — UPI, Credit Card, COD, etc. |
| `05_quarterly_revenue.png` | Bar chart — Q1 to Q4 comparison |
| `06_avg_rating.png` | Bar chart — customer ratings per category |
| `Sales_Analysis_Report.xlsx` | Multi-sheet Excel report with KPI summary |

---

## 🧹 Data Cleaning Steps

1. **Remove duplicate rows** (~1% intentionally introduced)
2. **Fix missing values** — `unit_price` filled with category median; `total_amount` recalculated
3. **Fix data types** — parse dates, round floats
4. **Feature engineering** — extract `month`, `month_name`, `quarter`, `day_of_week`, `is_weekend`

---

## 🗃️ SQL Queries (SQLite)

| Query | Purpose |
|---|---|
| `get_monthly_revenue` | Orders + revenue + avg order value per month |
| `get_category_performance` | Revenue, units sold, avg rating per category |
| `get_top_cities` | Top 10 cities by revenue |
| `get_payment_distribution` | Payment method usage % |
| `get_top_products` | Top 10 products by revenue |
| `get_quarterly_summary` | Revenue grouped by quarter |

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Pandas** — Data manipulation & transformation
- **Matplotlib** — Chart generation
- **SQLite3** — SQL queries (built into Python, no setup needed)
- **openpyxl** — Excel report generation
- **NumPy** — Numerical operations

---

## 👤 Author

**Yuvraj**  
Computer Science Graduate | Aspiring Data Analyst  
[LinkedIn](#) · [GitHub](#)

---

## 📝 License

This project is open source under the [MIT License](LICENSE).
