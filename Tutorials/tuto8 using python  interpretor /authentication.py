from database import accounts_db

def user_login():
    print_database("Initial")
    print("Welcome to the User Account System!")
    id_number = input("Please enter your ID number: ")
    password = input("Please enter your password: ")

    user_account = authenticate_user(id_number, password)
    if user_account:
        print("Login successful!")
        return user_account
    else:
        print("Invalid ID or password.")
        return None

def authenticate_user(id_number, password):
    for account in accounts_db.values():
        if account["id_number"] == id_number and account["password"] == password:
            return account
    return None
