"""
sql_analysis.py
---------------
Loads the cleaned data into an in-memory SQLite database and runs
business-insight SQL queries using Python's built-in sqlite3 module.
"""

import sqlite3
import pandas as pd


def load_into_sqlite(df: pd.DataFrame) -> sqlite3.Connection:
    """Create an in-memory SQLite DB and load the DataFrame as a table."""
    conn = sqlite3.connect(":memory:")
    df.to_sql("sales", conn, if_exists="replace", index=False)
    print("🗃️   Data loaded into SQLite  (in-memory)")
    return conn


def run_query(conn: sqlite3.Connection, sql: str) -> pd.DataFrame:
    """Helper: execute a SQL query and return results as a DataFrame."""
    return pd.read_sql_query(sql, conn)


def get_monthly_revenue(conn: sqlite3.Connection) -> pd.DataFrame:
    """Total revenue and order count per month."""
    sql = """
        SELECT
            month,
            month_name,
            COUNT(order_id)        AS total_orders,
            ROUND(SUM(total_amount), 2) AS total_revenue,
            ROUND(AVG(total_amount), 2) AS avg_order_value
        FROM sales
        GROUP BY month, month_name
        ORDER BY month;
    """
    return run_query(conn, sql)


def get_category_performance(conn: sqlite3.Connection) -> pd.DataFrame:
    """Revenue, units sold, and avg rating per category."""
    sql = """
        SELECT
            category,
            COUNT(order_id)             AS total_orders,
            SUM(quantity)               AS units_sold,
            ROUND(SUM(total_amount), 2) AS total_revenue,
            ROUND(AVG(rating), 2)       AS avg_rating
        FROM sales
        GROUP BY category
        ORDER BY total_revenue DESC;
    """
    return run_query(conn, sql)


def get_top_cities(conn: sqlite3.Connection, top_n: int = 10) -> pd.DataFrame:
    """Top N cities by total revenue."""
    sql = f"""
        SELECT
            customer_city,
            customer_state,
            COUNT(order_id)             AS total_orders,
            ROUND(SUM(total_amount), 2) AS total_revenue
        FROM sales
        GROUP BY customer_city, customer_state
        ORDER BY total_revenue DESC
        LIMIT {top_n};
    """
    return run_query(conn, sql)


def get_payment_distribution(conn: sqlite3.Connection) -> pd.DataFrame:
    """Count and percentage of orders per payment method."""
    sql = """
        SELECT
            payment_method,
            COUNT(order_id) AS order_count,
            ROUND(100.0 * COUNT(order_id) / (SELECT COUNT(*) FROM sales), 2) AS percentage
        FROM sales
        GROUP BY payment_method
        ORDER BY order_count DESC;
    """
    return run_query(conn, sql)


def get_top_products(conn: sqlite3.Connection, top_n: int = 10) -> pd.DataFrame:
    """Top N products by revenue."""
    sql = f"""
        SELECT
            product_name,
            category,
            SUM(quantity)               AS units_sold,
            ROUND(SUM(total_amount), 2) AS total_revenue,
            ROUND(AVG(rating), 2)       AS avg_rating
        FROM sales
        GROUP BY product_name, category
        ORDER BY total_revenue DESC
        LIMIT {top_n};
    """
    return run_query(conn, sql)


def get_quarterly_summary(conn: sqlite3.Connection) -> pd.DataFrame:
    """Revenue breakdown by quarter."""
    sql = """
        SELECT
            quarter,
            COUNT(order_id)             AS total_orders,
            ROUND(SUM(total_amount), 2) AS total_revenue,
            ROUND(AVG(total_amount), 2) AS avg_order_value
        FROM sales
        GROUP BY quarter
        ORDER BY quarter;
    """
    return run_query(conn, sql)


def run_all_queries(conn: sqlite3.Connection) -> dict:
    """Run every query and return results as a dict of DataFrames."""
    results = {
        "monthly_revenue":      get_monthly_revenue(conn),
        "category_performance": get_category_performance(conn),
        "top_cities":           get_top_cities(conn),
        "payment_distribution": get_payment_distribution(conn),
        "top_products":         get_top_products(conn),
        "quarterly_summary":    get_quarterly_summary(conn),
    }
    print("✅  All SQL queries executed successfully")
    return results


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from data_cleaning import run_cleaning_pipeline

    df = run_cleaning_pipeline()
    conn = load_into_sqlite(df)
    results = run_all_queries(conn)

    for name, frame in results.items():
        print(f"\n── {name} ──")
        print(frame.to_string(index=False))
