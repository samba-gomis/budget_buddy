import customtkinter as ctk
from repositories.account_model import get_balance
from repositories.transaction_repo import get_by_month
from datetime import datetime


def build_summary_cards(parent, account_id: int):
    """Builds the 3 summary cards and packs them into parent"""
    income, expenses = _get_monthly_totals(account_id)
    balance = get_balance(account_id) if account_id else 0.0
    month_label = datetime.now().strftime("%B %Y")

    ctk.CTkLabel(parent, text="Overview",
                 font=("Roboto", 16, "bold")).pack(anchor="w", pady=(10, 6))

    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", pady=(0, 16))
    row.columnconfigure((0, 1, 2), weight=1)

    cards = [
        ("Current balance",         f"{balance:.2f} €",   "#2ecc71" if balance >= 0 else "#e74c3c"),
        (f"Income — {month_label}", f"+{income:.2f} €",   "#3498db"),
        (f"Expenses — {month_label}", f"-{expenses:.2f} €", "#e67e22"),
    ]

    for col, (title, value, color) in enumerate(cards):
        card = ctk.CTkFrame(row, corner_radius=12)
        card.grid(row=0, column=col, padx=6, sticky="ew")
        ctk.CTkLabel(card, text=title,
                     font=("Roboto", 11), text_color="gray").pack(pady=(14, 2))
        ctk.CTkLabel(card, text=value,
                     font=("Roboto", 22, "bold"),
                     text_color=color).pack(pady=(0, 14))


def _get_monthly_totals(account_id: int) -> tuple[float, float]:
    if not account_id:
        return 0.0, 0.0
    now = datetime.now()
    transactions = get_by_month(account_id, now.year, now.month)
    income   = sum(t["amount"] for t in transactions if t["type"] == "deposit")
    expenses = sum(t["amount"] for t in transactions if t["type"] == "withdrawal")
    return round(income, 2), round(expenses, 2)