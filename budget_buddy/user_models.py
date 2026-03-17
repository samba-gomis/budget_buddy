import sqlite3
from databases.database import *

def create_user(last_name, first_name, email, password):

    conn=get_connection()
    cursor=conn.cursor()

    try:
        request="INSERT INTO users (last_name, first_name, email, password) VALUES (?,?,?,?)"
        values=(last_name, first_name, email, password)
        cursor.execute(request, values)
        conn.commit()

    except sqlite3.IntegrityError:
        print("Error, E-mail already used")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def get_user(email):

    conn=get_connection()
    cursor=conn.cursor()

    try:
        request="SELECT * from user WHERE email=?"
        value=(email,)
        cursor.execute(request,value)
        return cursor.fetchall()
    
    finally:
        conn.close()
        

  


