from repositories.user_models import create_user, get_user
from repositories.account_model import create_account
from repositories.validators import check_email, check_password, password_match
from repositories.User import User
import bcrypt

def verify_user_login(email: str, password: str) -> User | None:
    """
    Verifies login credentials.
    Returns a User object on success, or None if credentials are invalid.
    """
    user = get_user(email)
    if user is None:
        return None
    if bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return User(id=user["id"], last_name=user["last_name"],
                    first_name=user["first_name"], email=user["email"])
    return None


def register(last_name: str, first_name: str, email: str,
             password: str, confirm_password: str) -> tuple[bool, str]:
    """
    Registers a new user after validating all inputs.
    Returns (True, success_message) or (False, error_message).
    """
    valid, error = check_email(email)
    if not valid:
        return False, error

    valid, error = check_password(password)
    if not valid:
        return False, error

    valid, error = password_match(password, confirm_password)
    if not valid:
        return False, error

    # Create the user in the database
    create_user(last_name, first_name, email, password)

    # Retrieve the new user to get their ID
    new_user = get_user(email)

    # Create a linked bank account for this user
    create_account(new_user["id"])

    return True, f"{first_name} successfully created!"