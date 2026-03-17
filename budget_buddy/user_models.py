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
        request="SELECT * from users WHERE email=?"
        value=(email,)
        cursor.execute(request,value)
        return cursor.fetchall()
    
    finally:
        conn.close()

def update_user_profile(column_name, new_value,user_id):

    conn=get_connection()
    cursor=conn.cursor()

    try:
        request=f"UPDATE users SET {column_name}=? WHERE id=?"
        values=(new_value,user_id)
        cursor.execute(request,values)
        conn.commit()
       
    except sqlite3.IntegrityError:
        print("Error, something already exist")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def delete_user(user_id):

    conn=get_connection()
    cursor=conn.cursor()

    try:
        request="DELETE from users WHERE id=?"
        value=(user_id,)
        cursor.execute(request, value)
        conn.commit()
        
        if cursor.rowcount>0:
            print(f"{user_id} successfully deleted!")
            return True
        else:
            print(f"{user_id} doesn't exist")
            return False
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
    

    

        
        

  


