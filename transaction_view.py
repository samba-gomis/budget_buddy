# gui/transactions_view.py
# Displays the transaction history with search and filter options

import tkinter as tk
from tkinter import ttk, messagebox
from services import transaction_service


class Transactions_View(tk.Frame):
    """
    Transaction history view.
    Allows the user to browse, search, and filter their transactions.
    """

    def __init__(self, parent, account_id: int):
        super().__init__(parent, bg="#f5f6fa")
        self.account_id = account_id
        self._build_ui()
        self._load_transactions()


    def _build_ui(self):
        """Builds the full layout: title, filter bar, and transaction table."""
        self._build_title()
        self._build_filter_bar()
        self._build_table()

    def _build_title(self):
        tk.Label(
            self,
            text="Transaction History",
            font=("Helvetica", 18, "bold"),
            bg="#f5f6fa",
            fg="#2d3436"
        ).pack(anchor="w", padx=24, pady=(20, 4))

        tk.Label(
            self,
            text="Search and filter your transactions below.",
            font=("Helvetica", 11),
            bg="#f5f6fa",
            fg="#636e72"
        ).pack(anchor="w", padx=24, pady=(0, 12))

    def _build_filter_bar(self):
        """Builds the row of filters: date, type, category, amount sort, and reset."""
        bar = tk.Frame(self, bg="#ffffff", relief="flat", bd=0)
        bar.pack(fill="x", padx=24, pady=(0, 12))
        bar.configure(highlightbackground="#dfe6e9", highlightthickness=1)

        inner = tk.Frame(bar, bg="#ffffff", padx=16, pady=12)
        inner.pack(fill="x")

        # Row 1: date range + type + category
        row1 = tk.Frame(inner, bg="#ffffff")
        row1.pack(fill="x", pady=(0, 8))

        # Start date
        tk.Label(row1, text="From", bg="#ffffff", fg="#636e72",
                 font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", padx=(0, 4))
        self.start_date_var = tk.StringVar()
        tk.Entry(row1, textvariable=self.start_date_var, width=12,
                 font=("Helvetica", 10)).grid(row=0, column=1, padx=(0, 12))

        # End date
        tk.Label(row1, text="To", bg="#ffffff", fg="#636e72",
                 font=("Helvetica", 10)).grid(row=0, column=2, sticky="w", padx=(0, 4))
        self.end_date_var = tk.StringVar()
        tk.Entry(row1, textvariable=self.end_date_var, width=12,
                 font=("Helvetica", 10)).grid(row=0, column=3, padx=(0, 20))

        # Type filter
        tk.Label(row1, text="Type", bg="#ffffff", fg="#636e72",
                 font=("Helvetica", 10)).grid(row=0, column=4, sticky="w", padx=(0, 4))
        self.type_var = tk.StringVar(value="All")
        type_menu = ttk.Combobox(
            row1, textvariable=self.type_var,
            values=["All", "deposit", "withdrawal", "transfer"],
            state="readonly", width=12, font=("Helvetica", 10)
        )
        type_menu.grid(row=0, column=5, padx=(0, 20))

        # Category filter
        tk.Label(row1, text="Category", bg="#ffffff", fg="#636e72",
                 font=("Helvetica", 10)).grid(row=0, column=6, sticky="w", padx=(0, 4))
        self.category_var = tk.StringVar(value="All")
        category_menu = ttk.Combobox(
            row1, textvariable=self.category_var,
            values=["All", "leisure", "food", "transport",
                    "health", "housing", "salary", "savings", "other"],
            state="readonly", width=12, font=("Helvetica", 10)
        )
        category_menu.grid(row=0, column=7, padx=(0, 20))

        # Row 2: amount sort + buttons
        row2 = tk.Frame(inner, bg="#ffffff")
        row2.pack(fill="x")

        tk.Label(row2, text="Sort by amount", bg="#ffffff", fg="#636e72",
                 font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", padx=(0, 4))
        self.sort_var = tk.StringVar(value="None")
        sort_menu = ttk.Combobox(
            row2, textvariable=self.sort_var,
            values=["None", "Ascending", "Descending"],
            state="readonly", width=12, font=("Helvetica", 10)
        )
        sort_menu.grid(row=0, column=1, padx=(0, 20))

        # Apply button
        tk.Button(
            row2, text="Apply filters",
            command=self._apply_filters,
            bg="#0984e3", fg="white",
            font=("Helvetica", 10, "bold"),
            relief="flat", padx=14, pady=4,
            cursor="hand2", activebackground="#74b9ff"
        ).grid(row=0, column=2, padx=(0, 8))

        # Reset button
        tk.Button(
            row2, text="Reset",
            command=self._reset_filters,
            bg="#dfe6e9", fg="#2d3436",
            font=("Helvetica", 10),
            relief="flat", padx=14, pady=4,
            cursor="hand2", activebackground="#b2bec3"
        ).grid(row=0, column=3)

    def _build_table(self):
        """Builds the scrollable transaction table."""
        container = tk.Frame(self, bg="#f5f6fa")
        container.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(container, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = ttk.Scrollbar(container, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        # Treeview (table)
        columns = ("reference", "date", "type", "category", "description", "amount")
        self.table = ttk.Treeview(
            container,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            selectmode="browse"
        )

        # Column headers and widths
        headers = {
            "reference":   ("Reference",   120),
            "date":        ("Date",         140),
            "type":        ("Type",          90),
            "category":    ("Category",     100),
            "description": ("Description",  220),
            "amount":      ("Amount (€)",   100),
        }
        for col, (label, width) in headers.items():
            self.table.heading(col, text=label, anchor="w")
            self.table.column(col, width=width, anchor="w", minwidth=60)

        # Row colors for deposit / withdrawal / transfer
        self.table.tag_configure("deposit",    foreground="#00b894")
        self.table.tag_configure("withdrawal", foreground="#d63031")
        self.table.tag_configure("transfer",   foreground="#0984e3")
        self.table.tag_configure("even",       background="#f8f9fa")
        self.table.tag_configure("odd",        background="#ffffff")

        scrollbar_y.config(command=self.table.yview)
        scrollbar_x.config(command=self.table.xview)
        self.table.pack(fill="both", expand=True)

        # Summary label below the table
        self.summary_var = tk.StringVar()
        tk.Label(
            self, textvariable=self.summary_var,
            bg="#f5f6fa", fg="#636e72",
            font=("Helvetica", 10)
        ).pack(anchor="e", padx=24, pady=(0, 8))


    def _load_transactions(self, transactions: list[dict] | None = None):
        """
        Populates the table.
        If transactions is None, loads all transactions from the service.
        """
        # Clear existing rows
        for row in self.table.get_children():
            self.table.delete(row)

        if transactions is None:
            transactions = transaction_service.get_all(self.account_id)

        if not transactions:
            self.summary_var.set("No transactions found.")
            return

        total_in  = 0.0
        total_out = 0.0

        for i, t in enumerate(transactions):
            amount    = t["amount"]
            type_     = t["type"]
            category  = t.get("category_name") or "—"
            tag_row   = "even" if i % 2 == 0 else "odd"

            if type_ == "deposit":
                amount_str = f"+{amount:.2f}"
                total_in  += amount
            elif type_ == "withdrawal":
                amount_str = f"-{amount:.2f}"
                total_out += amount
            else:
                amount_str = f"{amount:.2f}"

            self.table.insert(
                "", "end",
                values=(
                    t["reference"],
                    t["date"],
                    type_,
                    category,
                    t.get("description") or "—",
                    amount_str,
                ),
                tags=(type_, tag_row)
            )

        self.summary_var.set(
            f"{len(transactions)} transaction(s) — "
            f"Total in: +{total_in:.2f} €  |  Total out: -{total_out:.2f} €"
        )


    def _apply_filters(self):
        """Reads the filter inputs and fetches the matching transactions."""
        start   = self.start_date_var.get().strip()
        end     = self.end_date_var.get().strip()
        type_   = self.type_var.get()
        cat     = self.category_var.get()
        sort    = self.sort_var.get()

        try:
            transactions = transaction_service.get_all(self.account_id)

            # Date range filter
            if start and end:
                transactions = transaction_service.filter_by_range(
                    self.account_id, start, end
                )
            elif start:
                transactions = transaction_service.filter_by_date(
                    self.account_id, start
                )

            # Type filter
            if type_ != "All":
                transactions = [t for t in transactions if t["type"] == type_]

            # Category filter
            if cat != "All":
                transactions = [
                    t for t in transactions if t.get("category_name") == cat
                ]

            # Amount sort
            if sort == "Ascending":
                transactions.sort(key=lambda t: t["amount"])
            elif sort == "Descending":
                transactions.sort(key=lambda t: t["amount"], reverse=True)

            self._load_transactions(transactions)

        except Exception as e:
            messagebox.showerror("Filter error", str(e))

    def _reset_filters(self):
        """Clears all filters and reloads all transactions."""
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.type_var.set("All")
        self.category_var.set("All")
        self.sort_var.set("None")
        self._load_transactions()