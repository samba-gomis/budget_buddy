from databases.database import *
from user_models import *
from validators import *

class User:
    def __init__(self, id, last_name, first_name, email):
        self.user_id=id
        self.first_name=first_name
        self.last_name=last_name
        self.email=email

    def __str__(self):
        return f"User: {self.first_name} {self.last_name} {self.email}"
        