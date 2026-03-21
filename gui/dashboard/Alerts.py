# gui/dashboard/alerts.py
# Alert banners (overdraft, low balance, no transactions)

import customtkinter as ctk
from repositories.account_model import get_balance
from repositories.transaction_repo import get_by_month
from datetime import datetime


def get_alerts(account_id: int) -> list[str]:
    """Returns a list of alert messages for the current account."""
    if not account_id:
        return ["No bank account found for this user."]

    alerts = []
    balance = get_balance(account_id)

    if balance < 0:
        alerts.append(f"⚠ Overdraft! Your balance is {balance:.2f} €")
    elif balance < 50:
        alerts.append(f"⚠ Low balance: only {balance:.2f} € remaining.")

    now = datetime.now()
    if not get_by_month(account_id, now.year, now.month):
        alerts.append("ℹ No transactions recorded this month.")

    return alerts


def build_alerts(parent, account_id: int):
    """Builds and packs alert banners into parent. Does nothing if no alerts."""
    alerts = get_alerts(account_id)
    if not alerts:
        return

    ctk.CTkLabel(parent, text="Alerts",
                 font=("Roboto", 16, "bold")).pack(anchor="w", pady=(0, 6))

    for alert in alerts:
        frame = ctk.CTkFrame(parent, fg_color="#fff3cd", corner_radius=8)
        frame.pack(fill="x", pady=2)
        ctk.CTkLabel(frame, text=alert,
                     font=("Roboto", 12),
                     text_color="#856404").pack(anchor="w", padx=14, pady=8)