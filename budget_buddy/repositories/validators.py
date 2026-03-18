import re
from user_models import *

def check_email(email):
    pattern= r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if re.match(pattern,email):
        return True
    else:
        return False
    
def check_password(password):
    
    if len(password)<10:
        return False, "Error! password must be at least 10 characters"
    
    if not any(char.isdigit() for char in password):
        return False, "Error! Password need at least one number!"
   
    if not any(char.isupper() for char in password):
        return False, "Error! Must contain at least one capital!"
  
    return True

def password_match(pass1,pass2):
    if pass1==pass2:
        return True
