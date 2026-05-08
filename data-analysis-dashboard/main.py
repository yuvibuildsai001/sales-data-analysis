"""
main.py
-------
Orchestrates the full data analysis pipeline:

    Step 1  →  Generate synthetic dataset
    Step 2  →  Clean & transform data
    Step 3  →  Load into SQLite & run SQL queries
    Step 4  →  Generate Matplotlib charts
    Step 5  →  Export Excel report

Run with:  python main.py
"""

import sys
import os
import time

# Make sure src/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from generate_data     import generate_sales_data
from data_cleaning     import run_cleaning_pipeline
from sql_analysis      import load_into_sqlite, run_all_queries
from visualizations    import generate_all_charts
from report_generator  import generate_excel_report


def banner(text: str) -> None:
    width = 55
    print("\n" + "═" * width)
    print(f"  {text}")
    print("═" * width)


def main():
    start = time.time()

    banner("STEP 1 — Generating Dataset")
    generate_sales_data(n_records=1000)

    banner("STEP 2 — Cleaning & Transforming Data")
    df_clean = run_cleaning_pipeline()

    banner("STEP 3 — SQL Analysis (SQLite)")
    conn         = load_into_sqlite(df_clean)
    sql_results  = run_all_queries(conn)

    banner("STEP 4 — Generating Charts (Matplotlib)")
    chart_paths  = generate_all_charts(sql_results)

    banner("STEP 5 — Exporting Excel Report")
    report_path  = generate_excel_report(df_clean, sql_results)

    elapsed = time.time() - start
    banner(f"✅  Pipeline Complete  ({elapsed:.1f}s)")
    print(f"""
  Output Summary
  ──────────────────────────────────────────────
  📁  Clean data   →  data/processed/sales_clean.csv
  📊  Charts       →  reports/*.png  ({len(chart_paths)} files)
  📄  Excel report →  {report_path}
  ──────────────────────────────────────────────
""")


if __name__ == "__main__":
    main()
