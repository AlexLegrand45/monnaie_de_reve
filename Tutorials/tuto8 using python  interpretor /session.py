from database import update_account

def user_session(user_account):
    user_id = [uid for uid, acc in accounts_db.items() if acc == user_account][0]
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
            exec(user_input, globals(), user_vars)
            print("Updated account details:", user_vars)
        except Exception as e:
            print(f"An error occurred: {e}")

    update_account(user_id, user_vars)
