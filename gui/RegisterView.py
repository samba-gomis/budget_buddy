# gui/RegisterView.py

from repositories.auth_service import register
import customtkinter as ctk
from tkinter import messagebox


class RegisterView(ctk.CTk):
    def __init__(self, on_login_click):
        super().__init__()
        self.on_login_click = on_login_click

        self.title("Budget Buddy — Register")
        self.geometry("500x600")

        ctk.CTkLabel(
            self, text="Welcome to Budget Buddy!", font=("Roboto", 28)
        ).pack(pady=40)

        self.last_name_entry = ctk.CTkEntry(
            self, placeholder_text="Last name", width=250
        )
        self.last_name_entry.pack(pady=10)

        self.first_name_entry = ctk.CTkEntry(
            self, placeholder_text="First name", width=250
        )
        self.first_name_entry.pack(pady=10)

        self.email_entry = ctk.CTkEntry(
            self, placeholder_text="Email", width=250
        )
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self, placeholder_text="Password", show="*", width=250
        )
        self.password_entry.pack(pady=10)

        self.confirm_password_entry = ctk.CTkEntry(
            self, placeholder_text="Confirm password", show="*", width=250
        )
        self.confirm_password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Register", command=self.registering).pack(pady=20)

        ctk.CTkButton(
            self, text="Already have an account? Login",
            command=self.on_login_click
        ).pack(pady=10)

    def registering(self):
        last_name          = self.last_name_entry.get().strip()
        first_name         = self.first_name_entry.get().strip()
        email              = self.email_entry.get().strip()
        password           = self.password_entry.get()
        confirmed_password = self.confirm_password_entry.get()

        if not all([last_name, first_name, email, password, confirmed_password]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        success, message = register(
            last_name, first_name, email, password, confirmed_password
        )

        if success:
            messagebox.showinfo("Success", message)
            self.on_login_click()
        else:
            messagebox.showerror("Error", message)