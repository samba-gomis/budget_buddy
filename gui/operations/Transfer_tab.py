# gui/operations/transfer_tab.py

import customtkinter as ctk
from tkinter import messagebox
from repositories.account_model import get_balance, get_accounts_by_user
from repositories.user_models import get_user
from repositories.account import Account


def build_transfer_tab(parent, account_id: int, on_done=None):
    """Builds the transfer form inside the given tab."""

    ctk.CTkLabel(parent, text="Recipient email",
                 font=("Roboto", 12)).pack(anchor="w", padx=20, pady=(16, 2))
    email_entry = ctk.CTkEntry(parent, placeholder_text="email@example.com",
                               width=300)
    email_entry.pack(padx=20)

    ctk.CTkLabel(parent, text="Amount (€)",
                 font=("Roboto", 12)).pack(anchor="w", padx=20, pady=(12, 2))
    amount_var = ctk.StringVar()
    ctk.CTkEntry(parent, textvariable=amount_var,
                 placeholder_text="0.00", width=300).pack(padx=20)

    ctk.CTkLabel(parent, text="Description (optional)",
                 font=("Roboto", 12)).pack(anchor="w", padx=20, pady=(12, 2))
    desc_entry = ctk.CTkEntry(parent, placeholder_text="e.g. Rent payment",
                              width=300)
    desc_entry.pack(padx=20)

    def confirm():
        recipient_email = email_entry.get().strip()
        if not recipient_email:
            messagebox.showerror("Error", "Please enter a recipient email.")
            return

        try:
            amount = float(amount_var.get().strip().replace(",", "."))
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive amount.")
            return

        try:
            recipient_user = get_user(recipient_email)
            if not recipient_user:
                messagebox.showerror("Error", "No account found with this email.")
                return

            recipient_accounts = get_accounts_by_user(recipient_user["id"])
            if not recipient_accounts:
                messagebox.showerror("Error", "Recipient has no bank account.")
                return

            sender           = Account(account_id=account_id)
            sender.balance   = get_balance(account_id)
            recipient        = Account(account_id=recipient_accounts[0]["id"])
            recipient.balance = recipient_accounts[0]["balance"]

            sender.transferer(
                amount=amount,
                compte_destinataire=recipient,
                description=desc_entry.get().strip() or "Transfer",
            )
            messagebox.showinfo("Success",
                                f"{amount:.2f} € transferred to {recipient_email}.")
            email_entry.delete(0, "end")
            amount_var.set("")
            desc_entry.delete(0, "end")
            if on_done:
                on_done()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(parent, text="Confirm transfer",
                  fg_color="#3498db", hover_color="#2980b9",
                  command=confirm).pack(pady=(16, 0))