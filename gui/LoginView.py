# gui/LoginView.py

from repositories.auth_service import verify_user_login
import customtkinter as ctk
from tkinter import messagebox


class LoginView(ctk.CTk):
    def __init__(self, on_register_click, on_login_success):
        super().__init__()
        self.on_register_click  = on_register_click
        self.on_login_success   = on_login_success

        self.title("Budget Buddy — Login")
        self.geometry("400x500")

        ctk.CTkLabel(self, text="Welcome!", font=("Roboto", 24)).pack(pady=40)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email", width=250)
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self, placeholder_text="Password", show="*", width=250
        )
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Login", command=self.login_event).pack(pady=20)

        ctk.CTkButton(
            self, text="No account yet? Register",
            command=self.on_register_click
        ).pack(pady=10)

    def login_event(self):
        email    = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        user = verify_user_login(email, password)

        if user:
            messagebox.showinfo("Success", f"Welcome back, {user.first_name}!")
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Wrong email or password.")