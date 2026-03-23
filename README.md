# Budget Buddy 

A personal finance management desktop application built with Python and CustomTkinter.
Budget Buddy allows users to track their accounts, manage transactions, and get a clear overview of their financial situation.

---

## Features

- **Secure authentication** — Register and login with a hashed password (bcrypt)
- **Password policy** — Minimum 10 characters, uppercase, lowercase, digit and special character required
- **Dashboard** — Overview of balance, monthly income/expenses, spending chart and alerts
- **Transactions** — Full history with search and filters (date, type, category, amount)
- **Operations** — Deposit, withdraw and transfer money between accounts
- **Alerts** — Automatic notifications for overdraft and low balance

---

## Project Structure

```
budget_buddy/
├── main.py                        # Entry point
├── requirements.txt               # Dependencies
├── LICENSE                        # MIT License
│
├── databases/
│   ├── __init__.py
│   ├── database.py                # Connection and initialization
│   └── models.py                  # SQL table schemas
│
├── repositories/
│   ├── __init__.py
│   ├── User.py                    # User data class
│   ├── account.py                 # Account class (deposit, withdraw, transfer)
│   ├── account_model.py           # Account database operations
│   ├── user_models.py             # User database operations
│   ├── transaction_repo.py        # Transaction database operations
│   ├── auth_service.py            # Login and registration logic
│   └── validators.py              # Email and password validation
│
├── services/
│   └── transaction_service.py     # Transaction business logic
│
└── gui/
    ├── LoginView.py               # Login screen
    ├── RegisterView.py            # Registration screen
    ├── DashboardView.py           # Main dashboard
    ├── OperationsView.py          # Operations panel
    ├── transaction_view.py        # Transaction history
    │
    ├── dashboard/
    │   ├── Summary_cards.py       # Balance and monthly summary cards
    │   ├── Alerts.py              # Alert banners
    │   ├── Chart.py               # Spending bar chart
    │   └── Recent_transactions.py # Recent transactions table
    │
    └── operations/
        ├── Deposit_tab.py         # Deposit form
        ├── Withdrawal_tab.py      # Withdrawal form
        └── Transfer_tab.py        # Transfer form
```

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourname/budget_buddy.git
cd budget_buddy
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the application**
```bash
python main.py
```

The database (`finance.db`) is created automatically on first launch.

---

## Dependencies

| Package | Usage |
|---|---|
| `customtkinter` | Modern graphical interface |
| `bcrypt` | Password hashing |
| `sqlite3` | Database (built into Python) |
| `tkinter` | Base GUI toolkit (built into Python) |

---

## Database Schema

```
users
├── id, last_name, first_name, email, password, created_at

accounts
├── id, user_id, balance, created_at

transactions
├── id, account_id, reference, description, amount, date, type, category_id, created_at

categories
└── id, name
```

---

## Password Requirements

To register, your password must contain:
- At least **10 characters**
- At least one **uppercase letter**
- At least one **lowercase letter**
- At least one **digit**
- At least one **special character** (!@#$%^&*...)

---

## Authors

- **Samba Diop Gomis**
- **Mahira Manico**
- **Moina Halima Abdoul**

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.