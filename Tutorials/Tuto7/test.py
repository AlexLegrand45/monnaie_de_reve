# Sample database of user accounts
accounts_db = {
    "user1": {
        "id_number": "1",
        "name": "John",
        "surname": "Doe",
        "password": "password123",  # In a real application, store hashed passwords
        "amount_of_tokens": 100
    },
    "user2": {
        "id_number": "2",
        "name": "Jane",
        "surname": "Smith",
        "password": "mypassword",  # In a real application, store hashed passwords
        "amount_of_tokens": 150
    }
}

def print_database(title):
    print(f"{title} Database:")
    for user_id, account in accounts_db.items():
        print(f"User ID: {user_id}, Account Details: {account}")

def user_login():
    print_database("Initial")
    print("Welcome to the User Account System!")
    id_number = input("Please enter your ID number: ")
    password = input("Please enter your password: ")

    # Find the user in the database
    user_account = None
    for account in accounts_db.values():
        if account["id_number"] == id_number and account["password"] == password:
            user_account = account
            break

    if user_account:
        print("Login successful!")
        user_session(user_account)
    else:
        print("Invalid ID or password.")

def user_session(user_account):
    # Create a copy of the user account without the ID and password
    user_vars = {
        "name": user_account["name"],
        "surname": user_account["surname"],
        "amount_of_tokens": user_account["amount_of_tokens"]
    }

    print(f"Welcome, {user_vars['name']} {user_vars['surname']}!")
    print("You can modify your account details. Type 'exit' to log out.")

    while True:
        user_input = input(">>> ")

        if user_input.lower() == 'exit':
            print("Logging out.")
            break

        try:
            # Execute the user's code with access to their account variables
            exec(user_input, globals(), user_vars)

            # Print the updated account variables
            print("Updated account details:", user_vars)
        except Exception as e:
            print(f"An error occurred: {e}")

    # Update the user account in the database with any changes
    user_account.update({
        "name": user_vars["name"],
        "surname": user_vars["surname"],
        "amount_of_tokens": user_vars["amount_of_tokens"]
    })

# Run the login system
user_login()

# Print the database at the end of the program
print_database("Final")