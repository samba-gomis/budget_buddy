from repositories.account_model import (create_account, get_accounts_by_user, get_balance, update_balance)
from repositories.transaction_repo import add as add_transaction
from datetime import datetime
import uuid


class Account:
    def __init__(self, account_id=None, user_id=None, balance=0.0):
        self.account_id = account_id
        self.user_id = user_id
        self.balance = balance

    def create(self):
        """Creates a new account for the user in the database"""
        self.account_id = create_account(self.user_id, self.balance)
        print(f"[Account] Account created for user {self.user_id}")

    def load(self, account_id: int):
        """Loads an existing account by ID"""
        accounts = get_accounts_by_user(self.user_id)
        for acc in accounts:
            if acc["id"] == account_id:
                self.account_id = acc["id"]
                self.balance = acc["balance"]
                return
        raise ValueError("Account not found")

    def deposit(self, amount: float, category_id=None, description="Deposit"):
        """Deposits money into the account"""
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero")
        self.balance += amount
        update_balance(self.account_id, self.balance)
        add_transaction(
            account_id=self.account_id,
            reference=self._generate_ref(),
            description=description,
            amount=amount,
            date=self._now(),
            type_="deposit",
            category_id=category_id
        )
        print(f"[Account] Deposited {amount}€ into account {self.account_id}")

    def withdraw(self, amount: float, category_id=None, description="Withdrawal"):
        """Withdraws money from the account"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero")
        if self.balance < amount:
            raise ValueError(f"Insufficient funds. Available: {self.balance:.2f}€")
        self.balance -= amount
        update_balance(self.account_id, self.balance)
        add_transaction(
            account_id=self.account_id,
            reference=self._generate_ref(),
            description=description,
            amount=amount,
            date=self._now(),
            type_="withdrawal",
            category_id=category_id
        )
        print(f"[Account] Withdrew {amount}€ from account {self.account_id}")

    def transfer(self, amount: float, destination_account,
                 category_id=None, description="Transfer"):
        """Transfers money to another Account instance"""
        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero")
        if self.account_id == destination_account.account_id:
            raise ValueError("Cannot transfer to the same account")
        self.withdraw(amount, category_id, description)
        destination_account.deposit(amount, category_id, description)
        print(f"[Account] Transferred {amount}€ from {self.account_id} "
              f"to {destination_account.account_id}")

    @staticmethod
    def _generate_ref() -> str:
        return str(uuid.uuid4()).replace("-", "")[:12].upper()

    @staticmethod
    def _now() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")