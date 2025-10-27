import matplotlib.pyplot as plt
from database import accounts_db

def read():
    user_ids = list(accounts_db.keys())
    names = [account['name'] for account in accounts_db.values()]
    surnames = [account['surname'] for account in accounts_db.values()]
    tokens = [account['amount_of_tokens'] for account in accounts_db.values()]

    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    axs[0].bar(user_ids, names, color='skyblue')
    axs[0].set_title('User Names')
    axs[0].set_ylabel('Name')

    axs[1].bar(user_ids, surnames, color='lightgreen')
    axs[1].set_title('User Surnames')
    axs[1].set_ylabel('Surname')

    axs[2].bar(user_ids, tokens, color='salmon')
    axs[2].set_title('User Tokens')
    axs[2].set_ylabel('Amount of Tokens')

    plt.tight_layout()
    plt.show()
