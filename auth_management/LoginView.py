from repositories.auth_service import *
from databases import *
import customtkinter as ctk
from tkinter import messagebox

class LoginView(ctk.CTk):
    def __init__(self, on_register_click):
        super().__init__()
        self.on_register_click=on_register_click
        self.title("Budget-Buddy Connexion page")
        self.geometry("400x500")

        self.label=ctk.CTkLabel(self, text="Welcome!", font=("Roboto", 24))
        self.label.pack(pady=40)

        self.email_entry=ctk.CTkEntry(self, placeholder_text="Email", width=250)
        self.email_entry.pack(pady=10)

        self.password_entry=ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=10)

        self.login_button=ctk.CTkButton(self, text="Login", command=self.login_event)
        self.login_button.pack(pady=20)

        self.register_link=ctk.CTkButton(self, text="No account yet? Register", command=self.on_register_click)
        self.register_link.pack(pady=10)

    def login_event(self):
        email=self.email_entry.get()
        password=self.password_entry.get()

        login=verify_user_login(email, password)

        if login:
            messagebox.showinfo(f"Success! Pleasure to see you again {login.first_name}")
        else:
            messagebox.showerror("Error! Wrong email or password!")
    
    def go_to_register(self):
        pass

