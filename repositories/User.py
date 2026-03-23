class User:
    """Simple data container representing a logged-in user"""

    def __init__(self, id: int, last_name: str, first_name: str, email: str):
        self.user_id    = id
        self.first_name = first_name
        self.last_name  = last_name
        self.email      = email

    def __str__(self):
        return f"User: {self.first_name} {self.last_name} ({self.email})"