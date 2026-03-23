import customtkinter as ctk
from tkinter import ttk
from repositories.transaction_repo import get_all


def build_recent_transactions(parent, account_id: int, limit: int = 5):
    """Builds and packs the recent transactions table into parent"""
    ctk.CTkLabel(parent, text="Recent transactions",
                 font=("Roboto", 16, "bold")).pack(anchor="w", pady=(0, 6))

    frame = ctk.CTkFrame(parent, corner_radius=12)
    frame.pack(fill="x", pady=(0, 16))

    transactions = get_all(account_id)[:limit] if account_id else []

    if not transactions:
        ctk.CTkLabel(frame, text="No transactions yet",
                     text_color="gray",
                     font=("Roboto", 12)).pack(pady=16)
        return

    style = ttk.Style()
    style.configure("Dashboard.Treeview",
                    rowheight=28, font=("Helvetica", 11))
    style.configure("Dashboard.Treeview.Heading",
                    font=("Helvetica", 11, "bold"))

    columns = ("date", "type", "category", "description", "amount")
    table = ttk.Treeview(frame, columns=columns, show="headings",
                         height=len(transactions), style="Dashboard.Treeview")

    headers = {
        "date":        ("Date",        130),
        "type":        ("Type",         90),
        "category":    ("Category",    100),
        "description": ("Description", 220),
        "amount":      ("Amount (€)",  100),
    }
    for col, (label, width) in headers.items():
        table.heading(col, text=label, anchor="w")
        table.column(col, width=width, anchor="w")

    table.tag_configure("deposit",    foreground="#2ecc71")
    table.tag_configure("withdrawal", foreground="#e74c3c")
    table.tag_configure("transfer",   foreground="#3498db")

    for t in transactions:
        amount = t["amount"]
        type_  = t["type"]
        prefix = "+" if type_ == "deposit" else "-" if type_ == "withdrawal" else ""
        table.insert("", "end",
            values=(
                t["date"][:16],
                type_,
                t.get("category_name") or "—",
                t.get("description") or "—",
                f"{prefix}{amount:.2f}",
            ),
            tags=(type_,)
        )

    table.pack(fill="x", padx=12, pady=12)