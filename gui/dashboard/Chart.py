# gui/dashboard/chart.py
# Bar chart of spending by category for the current month

import tkinter as tk
import customtkinter as ctk
from repositories.transaction_repo import get_by_month
from datetime import datetime

BAR_COLORS = ["#3498db", "#2ecc71", "#e67e22", "#9b59b6",
              "#1abc9c", "#e74c3c", "#f39c12", "#34495e"]


def build_chart(parent, account_id: int):
    """Builds and packs the spending bar chart into parent."""
    ctk.CTkLabel(parent, text="Spending by category (this month)",
                 font=("Roboto", 16, "bold")).pack(anchor="w", pady=(16, 6))

    frame = ctk.CTkFrame(parent, corner_radius=12, height=200)
    frame.pack(fill="x", pady=(0, 16))
    frame.pack_propagate(False)

    totals = _get_category_totals(account_id)

    if not totals:
        ctk.CTkLabel(frame, text="No spending data for this month.",
                     text_color="gray",
                     font=("Roboto", 12)).pack(expand=True)
        return

    canvas = tk.Canvas(frame, bg="#2b2b2b", highlightthickness=0, height=180)
    canvas.pack(fill="both", expand=True, padx=12, pady=10)
    canvas.bind("<Configure>", lambda e: _draw_bars(canvas, totals))


def _get_category_totals(account_id: int) -> dict:
    if not account_id:
        return {}
    now = datetime.now()
    transactions = get_by_month(account_id, now.year, now.month)
    totals = {}
    for t in transactions:
        if t["type"] == "withdrawal":
            cat = t.get("category_name") or "other"
            totals[cat] = round(totals.get(cat, 0) + t["amount"], 2)
    return totals


def _draw_bars(canvas, totals: dict):
    canvas.delete("all")
    w, h = canvas.winfo_width(), canvas.winfo_height()
    if w < 10 or h < 10:
        return

    categories = list(totals.keys())
    values     = list(totals.values())
    max_val    = max(values) if values else 1
    n          = len(categories)
    padding    = 40
    gap        = 12
    bar_w      = max(20, (w - 2 * padding - gap * (n - 1)) // n)
    chart_h    = h - 50

    for i, (cat, val) in enumerate(zip(categories, values)):
        x0    = padding + i * (bar_w + gap)
        x1    = x0 + bar_w
        bar_h = int((val / max_val) * chart_h)
        y0    = h - 30 - bar_h
        y1    = h - 30
        color = BAR_COLORS[i % len(BAR_COLORS)]

        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        canvas.create_text((x0 + x1) // 2, y1 + 10,
                           text=cat[:8], fill="white", font=("Helvetica", 9))
        canvas.create_text((x0 + x1) // 2, y0 - 10,
                           text=f"{val:.0f}€", fill="white", font=("Helvetica", 9))