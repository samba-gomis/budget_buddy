import customtkinter as ctk
from tkinter import messagebox
from repositories.account_model import get_balance
from repositories.Account import Account


def build_withdrawal_tab(parent, account_id: int, on_done=None):
    """Builds the withdrawal form inside the given tab"""

    ctk.CTkLabel(parent, text="Amount (€)",
                 font=("Roboto", 12)).pack(anchor="w", padx=20, pady=(16, 2))
    amount_var = ctk.StringVar()
    ctk.CTkEntry(parent, textvariable=amount_var,
                 placeholder_text="0.00", width=300).pack(padx=20)

    ctk.CTkLabel(parent, text="Description (optional)",
                 font=("Roboto", 12)).pack(anchor="w", padx=20, pady=(12, 2))
    desc_entry = ctk.CTkEntry(parent, placeholder_text="e.g. Grocery shopping",
                              width=300)
    desc_entry.pack(padx=20)

    ctk.CTkLabel(parent, text="Category",
                 font=("Roboto", 12)).pack(anchor="w", padx=20, pady=(12, 2))
    category_var = ctk.StringVar(value="other")
    ctk.CTkComboBox(
        parent,
        values=["leisure", "food", "transport", "health",
                "housing", "salary", "savings", "other"],
        variable=category_var, width=300
    ).pack(padx=20)

    def confirm():
        try:
            amount = float(amount_var.get().strip().replace(",", "."))
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive amount")
            return

        try:
            account = Account(account_id=account_id)
            account.balance = get_balance(account_id)
            account.withdraw(amount=amount,
                           description=desc_entry.get().strip() or "Withdrawal")
            messagebox.showinfo("Success", f"{amount:.2f} € withdrawn successfully")
            amount_var.set("")
            desc_entry.delete(0, "end")
            if on_done:
                on_done()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(parent, text="Confirm withdrawal",
                  fg_color="#e74c3c", hover_color="#c0392b",
                  command=confirm).pack(pady=(16, 0))