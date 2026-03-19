from repositories.auth_service import *
from databases import *
import customtkinter as ctk
from tkinter import messagebox


class RegisterView(ctk.CTk):
    def __init__(self, on_login_click):
        super().__init__()
        self.title("Budget-Buddy Register page")
        self.on_login_click=on_login_click
        self.geometry("500x600")
        
        self.label=ctk.CTkLabel(self, text="Welcome to Budget Buddy!", font=("Roboto",40))
        self.label.pack(pady=40)

        self.last_name_entry=ctk.CTkEntry(self, placeholder_text="Enter your last name", width=250)
        self.last_name_entry.pack(pady=10)

        self.first_name_entry=ctk.CTkEntry(self, placeholder_text="Enter your first name", width=250)
        self.first_name_entry.pack(pady=10)

        self.email_entry=ctk.CTkEntry(self, placeholder_text="Enter your Email", width=250)
        self.email_entry.pack(pady=10)

        self.password_entry=ctk.CTkEntry(self, placeholder_text="Enter your password", show="*", width=250)
        self.password_entry.pack(pady=10)

        self.confirm_password_entry=ctk.CTkEntry(self, placeholder_text="Confirm password", show="*", width=250)
        self.confirm_password_entry.pack(pady=10)

        self.valid_button=ctk.CTkButton(self, text="Valid", command=self.registering)
        self.valid_button.pack(pady=20)

        self.login_button=ctk.CTkButton(self, text="Login", command=self.on_login_click)

    
    def registering(self):

        last_name=self.last_name_entry.get()
        first_name=self.first_name_entry.get()
        email=self.email_entry.get()
        password=self.password_entry.get()
        confirmed_password=self.confirm_password_entry.get()

        success, message=register(last_name, first_name, email, password, confirmed_password)

        if success:
            messagebox.showinfo("Success!", message)
        else:
            messagebox.showerror("Error!", message)
