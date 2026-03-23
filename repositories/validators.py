import re

def check_email(email: str) -> tuple[bool, str]:
    pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if re.match(pattern, email):
        return True, ""
    return False, "Invalid email address"

def check_password(password: str) -> tuple[bool, str]:
    if len(password) < 10:
        return False, "Password must be at least 10 characters long"
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\+=/\\]", password):
        return False, "Password must contain at least one special character"
    return True, ""

def password_match(pass1: str, pass2: str) -> tuple[bool, str]:
    if pass1 == pass2:
        return True, ""
    return False, "Password do not match"