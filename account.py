# compte.py
from account_model import create_account, get_accounts_by_user, update_balance
from transaction_model import add_transaction
from datetime import datetime
import uuid

class Compte:
    def __init__(self, account_id=None, user_id=None, balance=0.0):
        self.account_id = account_id
        self.user_id = user_id
        self.balance = balance

    # Créer un compte pour un utilisateur
    def create(self):
        create_account(self.user_id, self.balance)
        print(f"[Compte] Compte créé pour l'utilisateur {self.user_id}")

    # Charger un compte existant (pour opérations)
    def load(self, account_id):
        accounts = get_accounts_by_user(self.user_id)
        for acc in accounts:
            if acc["id"] == account_id:
                self.account_id = acc["id"]
                self.balance = acc["balance"]
                return
        raise ValueError("Compte introuvable.")

    # Déposer de l'argent
    def deposer(self, amount, category_id=None, description="Dépôt"):
        self.balance += amount
        update_balance(self.account_id, self.balance)
        ref = str(uuid.uuid4())
        date = datetime.now().isoformat()
        add_transaction(self.account_id, ref, description, amount, date, "deposit", category_id)
        print(f"[Compte] Déposé {amount}€ sur le compte {self.account_id}")

    # Retirer de l'argent
    def retirer(self, amount, category_id=None, description="Retrait"):
        if self.balance < amount:
            raise ValueError("Solde insuffisant")
        self.balance -= amount
        update_balance(self.account_id, self.balance)
        ref = str(uuid.uuid4())
        date = datetime.now().isoformat()
        add_transaction(self.account_id, ref, description, amount, date, "withdrawal", category_id)
        print(f"[Compte] Retiré {amount}€ du compte {self.account_id}")

    # Transférer vers un autre compte
    def transferer(self, amount, compte_destinataire, category_id=None, description="Transfert"):
        self.retirer(amount, category_id, description)
        compte_destinataire.deposer(amount, category_id, description)
        print(f"[Compte] Transféré {amount}€ du compte {self.account_id} vers {compte_destinataire.account_id}")