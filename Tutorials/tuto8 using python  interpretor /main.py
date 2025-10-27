from authentication import user_login
from session import user_session
from visualization import read
from database import print_database

def main():
    user_account = user_login()
    if user_account:
        user_session(user_account)
        read()
    print_database("Final")

if __name__ == "__main__":
    main()
