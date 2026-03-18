from user_models import * 
from validators import *
import bcrypt

def verify_user_login(email,password):
    
    user=get_user(email)

    if user:
        if bcrypt.checkpw(password.encode("utf-8"), user['password']):
            return user
    return None

def register(last_name, first_name, email, password,confirm_password):

    if not check_email(email):
        return False, "Invalid Email"
    if not check_password(password):
        return False, "Invalid Password"
    if not password_match(password, confirm_password):
        return False, "Passwords doesn't match"
    
    create_user(last_name, first_name, email, password)
    return True, f"{first_name} successfuly created!"
   
