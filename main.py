from databases.database import init_db
from gui.LoginView import LoginView
from gui.RegisterView import RegisterView


def main():
    # Initialize the database (creates tables if they don't exist)
    init_db()

    app = None


    def show_login():
        nonlocal app
        try:
            if app and app.winfo_exists():
                app.destroy()
        except Exception:
            pass
        app = LoginView(
            on_register_click=show_register,
            on_login_success=show_dashboard
        )
        app.mainloop()


    def show_register():
        nonlocal app
        try:
            if app and app.winfo_exists():
                app.destroy()
        except Exception:
            pass
        app = RegisterView(on_login_click=show_login)
        app.mainloop()


    def show_dashboard(user):
        nonlocal app
        try:
            if app and app.winfo_exists():
                app.destroy()
        except Exception:
            pass

        # Import here to avoid circular imports
        from gui.dashboard.DashboardView import DashboardView
        app = DashboardView(user=user, on_logout=show_login)
        app.mainloop()

    show_login()


if __name__ == "__main__":
    main()