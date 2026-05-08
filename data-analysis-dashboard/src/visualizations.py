"""
visualizations.py
-----------------
Generates and saves 6 Matplotlib charts from the SQL query results.
All charts are saved to the reports/ folder.
"""

import matplotlib
matplotlib.use("Agg")          # Non-interactive backend (safe for scripts)

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import os

# ── Global style ───────────────────────────────────────────────────────────────
COLORS = ["#2563EB", "#16A34A", "#DC2626", "#D97706", "#7C3AED", "#0891B2"]
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor":   "#F8FAFC",
    "axes.spines.top":  False,
    "axes.spines.right": False,
    "font.family":      "DejaVu Sans",
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
})

OUTPUT_DIR = "reports"


def _save(fig: plt.Figure, filename: str) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"   📊  Saved  →  {path}")
    return path


# ── 1. Monthly Revenue Trend ───────────────────────────────────────────────────
def plot_monthly_revenue(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["month_name"], df["total_revenue"] / 1e6,
            marker="o", linewidth=2.5, color=COLORS[0], markersize=7)
    ax.fill_between(df["month_name"], df["total_revenue"] / 1e6,
                    alpha=0.12, color=COLORS[0])
    ax.set_title("Monthly Revenue Trend (2024)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (₹ Million)")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("₹%.1fM"))
    for x, y in zip(df["month_name"], df["total_revenue"] / 1e6):
        ax.annotate(f"₹{y:.1f}M", (x, y), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=8, color=COLORS[0])
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    return _save(fig, "01_monthly_revenue.png")


# ── 2. Revenue by Category ─────────────────────────────────────────────────────
def plot_category_revenue(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(df["category"], df["total_revenue"] / 1e6,
                  color=COLORS, edgecolor="white", linewidth=0.8)
    ax.set_title("Revenue by Product Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Revenue (₹ Million)")
    ax.bar_label(bars, labels=[f"₹{v:.1f}M" for v in df["total_revenue"] / 1e6],
                 padding=4, fontsize=9)
    ax.set_ylim(0, df["total_revenue"].max() / 1e6 * 1.18)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    return _save(fig, "02_category_revenue.png")


# ── 3. Top 10 Cities ───────────────────────────────────────────────────────────
def plot_top_cities(df: pd.DataFrame) -> str:
    df_sorted = df.sort_values("total_revenue")
    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.barh(df_sorted["customer_city"], df_sorted["total_revenue"] / 1e6,
                   color=COLORS[1], edgecolor="white")
    ax.set_title("Top 10 Cities by Revenue")
    ax.set_xlabel("Revenue (₹ Million)")
    ax.bar_label(bars, labels=[f"₹{v:.1f}M" for v in df_sorted["total_revenue"] / 1e6],
                 padding=4, fontsize=9)
    ax.set_xlim(0, df_sorted["total_revenue"].max() / 1e6 * 1.15)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    fig.tight_layout()
    return _save(fig, "03_top_cities.png")


# ── 4. Payment Method Distribution ────────────────────────────────────────────
def plot_payment_methods(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        df["order_count"],
        labels=df["payment_method"],
        autopct="%1.1f%%",
        colors=COLORS,
        startangle=140,
        pctdistance=0.78,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    for t in autotexts:
        t.set_fontsize(9)
    ax.set_title("Payment Method Distribution")
    fig.tight_layout()
    return _save(fig, "04_payment_methods.png")


# ── 5. Quarterly Revenue Comparison ───────────────────────────────────────────
def plot_quarterly_revenue(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(df["quarter"], df["total_revenue"] / 1e6,
                  color=COLORS[4], width=0.5, edgecolor="white")
    ax.set_title("Quarterly Revenue Comparison")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Revenue (₹ Million)")
    ax.bar_label(bars, labels=[f"₹{v:.1f}M" for v in df["total_revenue"] / 1e6],
                 padding=4, fontsize=10, fontweight="bold")
    ax.set_ylim(0, df["total_revenue"].max() / 1e6 * 1.15)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    return _save(fig, "05_quarterly_revenue.png")


# ── 6. Average Rating by Category ─────────────────────────────────────────────
def plot_avg_rating(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(df["category"], df["avg_rating"],
                  color=COLORS[2], edgecolor="white")
    ax.set_title("Average Customer Rating by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Average Rating (out of 5)")
    ax.set_ylim(0, 5.5)
    ax.axhline(y=4.0, color="gray", linestyle="--", alpha=0.5, label="Rating = 4.0")
    ax.bar_label(bars, labels=[f"{v:.2f} / 5" for v in df["avg_rating"]],
                 padding=4, fontsize=9)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    return _save(fig, "06_avg_rating.png")


# ── Master function ────────────────────────────────────────────────────────────
def generate_all_charts(sql_results: dict) -> list:
    """Generate all 6 charts. Returns list of saved file paths."""
    print("\n📈  Generating charts ...")
    paths = [
        plot_monthly_revenue(sql_results["monthly_revenue"]),
        plot_category_revenue(sql_results["category_performance"]),
        plot_top_cities(sql_results["top_cities"]),
        plot_payment_methods(sql_results["payment_distribution"]),
        plot_quarterly_revenue(sql_results["quarterly_summary"]),
        plot_avg_rating(sql_results["category_performance"]),
    ]
    print(f"✅  {len(paths)} charts saved to  '{OUTPUT_DIR}/'")
    return paths
