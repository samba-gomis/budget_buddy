# gui/DashboardView.py
# Main dashboard — assembles all dashboard components

import customtkinter as ctk
from tkinter import messagebox
from repositories.account_model import get_accounts_by_user
from gui.dashboard.Summary_cards import build_summary_cards
from gui.dashboard.Alerts import build_alerts
from gui.dashboard.Chart import build_chart
from gui.dashboard.Recent_transactions import build_recent_transactions


class DashboardView(ctk.CTk):

    def __init__(self, user, on_logout):
        super().__init__()
        self.user       = user
        self.on_logout  = on_logout
        self.account_id = self._load_account()

        self.title("Budget Buddy — Dashboard")
        self.geometry("900x650")
        self.resizable(True, True)
        self._build_ui()

    def _load_account(self) -> int | None:
        accounts = get_accounts_by_user(self.user.user_id)
        return accounts[0]["id"] if accounts else None

    def _build_ui(self):
        self._build_topbar()
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        build_summary_cards(scroll, self.account_id)
        build_alerts(scroll, self.account_id)
        build_chart(scroll, self.account_id)
        build_recent_transactions(scroll, self.account_id)

    def _build_topbar(self):
        bar = ctk.CTkFrame(self, height=56, corner_radius=0)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)

        ctk.CTkLabel(
            bar,
            text=f"Budget Buddy  —  {self.user.first_name} {self.user.last_name}",
            font=("Roboto", 15, "bold")
        ).pack(side="left", padx=20)

        ctk.CTkButton(bar, text="Logout", width=90,
                      fg_color="#e74c3c", hover_color="#c0392b",
                      command=self._logout).pack(side="right", padx=12, pady=10)

        ctk.CTkButton(bar, text="Transactions", width=110,
                      command=self._open_transactions).pack(side="right", padx=(0, 6), pady=10)

        ctk.CTkButton(bar, text="Operations", width=100,
                      command=self._open_operations).pack(side="right", padx=(0, 6), pady=10)

    def _open_transactions(self):
        if not self.account_id:
            messagebox.showwarning("Warning", "No account found.")
            return
        from gui.transaction_view import Transactions_View
        win = ctk.CTkToplevel(self)
        win.title("Transactions")
        win.geometry("900x600")
        Transactions_View(win, self.account_id).pack(fill="both", expand=True)

    def _open_operations(self):
        if not self.account_id:
            messagebox.showwarning("Warning", "No account found.")
            return
        try:
            from gui.OperationsView import OperationsView
            win = ctk.CTkToplevel(self)
            win.title("Operations")
            win.geometry("480x500")
            OperationsView(win, self.account_id,
                           on_operation_done=self._refresh).pack(fill="both", expand=True)
        except ImportError as e:
            messagebox.showerror("Import Error", str(e))

    def _refresh(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.account_id = self._load_account()
        self._build_ui()

    def _logout(self):
        self.destroy()
        self.on_logout()