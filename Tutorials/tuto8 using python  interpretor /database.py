"""
Database Management Module for Token-Based Access Control System

This module provides a structured way to manage user accounts and tokens with hierarchical access levels.
Each token has a `level` and a `self_level`, allowing fine-grained control over who can read or modify them.
Users can access or modify tokens based on their access level relative to the token's level or self_level.

Key Features:
- Token class to encapsulate data with access levels.
- Functions to create, read, update, and delete tokens and accounts.
- Support for both general and self-access levels.
"""

class Token:
    """
    Represents a data token with access control levels.

    Attributes:
        name (str): The name of the token.
        value: The value stored in the token.
        level (int): The access level required to read or modify this token.
        self_level (int): The access level required for self-read or self-modify operations.
    """
    def __init__(self, name, value, level, self_level):
        self.name = name
        self.value = value
        self.level = level
        self.self_level = self_level

    def __repr__(self):
        """Provides a string representation of the token."""
        return f"Token(name={self.name}, value={self.value}, level={self.level})"

# Global dictionary to store all user accounts
accounts_db = {}

def print_database(title):
    """
    Returns a string representation of the entire database.

    Args:
        title (str): A title for the database output.

    Returns:
        str: A formatted string containing all accounts and their details.
    """
    database_info = f"{title} Database:\n"
    for user_id, account in accounts_db.items():
        database_info += f"User ID: {user_id}, Account Details: {account}\n"
    return database_info

def print_account(user_id):
    """
    Returns a string representation of a specific account.

    Args:
        user_id (str): The ID of the account to print.

    Returns:
        str: A formatted string containing the account's details, or an error message if not found.
    """
    account = accounts_db.get(user_id)
    if account:
        account_info = f"Account Details for {user_id}:\n"
        for key, token in account.items():
            account_info += f"{key}: {token}\n"
        return account_info
    else:
        return "Account not found."

def get_token(user_id, token_name, requester_access_level):
    """
    Retrieves the value of a token if the requester has sufficient access level.

    Args:
        user_id (str): The ID of the user account.
        token_name (str): The name of the token to retrieve.
        requester_access_level (int): The access level of the requester.

    Returns:
        The token's value if access is granted, otherwise an error message.
    """
    account = accounts_db.get(user_id)
    if account:
        token = account.get(token_name)
        if token and requester_access_level <= token.level:
            return token.value
    return "Access denied or token not found."

def self_get_token(requester_id, token_name, requester_access_level):
    """
    Retrieves the value of a token for self-access if the requester has sufficient self-access level.

    Args:
        requester_id (str): The ID of the requester (must match the account ID).
        token_name (str): The name of the token to retrieve.
        requester_access_level (int): The access level of the requester.

    Returns:
        The token's value if self-access is granted, otherwise an error message.
    """
    account = accounts_db.get(requester_id)
    if account:
        token = account.get(token_name)
        if token and requester_access_level <= token.self_level:
            return token.value
    return "Access denied or token not found."

def update_token(user_id, token_name, new_value, requester_access_level):
    """
    Updates a token's value if the requester has sufficient access level.

    Args:
        user_id (str): The ID of the user account.
        token_name (str): The name of the token to update.
        new_value: The new value to set.
        requester_access_level (int): The access level of the requester.

    Returns:
        str: Success message if updated, otherwise an error message.
    """
    account = accounts_db.get(user_id)
    if account:
        token = account.get(token_name)
        if token and requester_access_level <= token.level:
            token.value = new_value
            return "Token updated successfully."
        else:
            return "Access denied: Insufficient user level."
    else:
        return "Account not found."

def self_update_token(requester_id, token_name, new_value, requester_access_level):
    """
    Updates a token's value for self-access if the requester has sufficient self-access level.

    Args:
        requester_id (str): The ID of the requester (must match the account ID).
        token_name (str): The name of the token to update.
        new_value: The new value to set.
        requester_access_level (int): The access level of the requester.

    Returns:
        str: Success message if updated, otherwise an error message.
    """
    account = accounts_db.get(requester_id)
    if account:
        token = account.get(token_name)
        if token and requester_access_level <= token.self_level:
            token.value = new_value
            return "Token updated successfully."
        else:
            return "Access denied: Insufficient user level for self update."
    else:
        return "Account not found."

def create_token(user_id, token_name, value, level, self_level):
    """
    Creates a new token in the specified account.

    Args:
        user_id (str): The ID of the user account.
        token_name (str): The name of the new token.
        value: The value of the new token.
        level (int): The access level for the new token.
        self_level (int): The self-access level for the new token.

    Returns:
        str: Success message if created, otherwise an error message.
    """
    token = Token(token_name, value, level, self_level)
    if user_id in accounts_db:
        accounts_db[user_id][token_name] = token
    else:
        accounts_db[user_id] = {token_name: token}
    return "Token created successfully."

def delete_token(user_id, token_name):
    """
    Deletes a token from the specified account.

    Args:
        user_id (str): The ID of the user account.
        token_name (str): The name of the token to delete.

    Returns:
        str: Success message if deleted, otherwise an error message.
    """
    account = accounts_db.get(user_id)
    if account and token_name in account:
        del account[token_name]
        return "Token deleted successfully."
    else:
        return "Token not found."

def create_account(account_details):
    """
    Creates a new user account with the provided details.

    Args:
        account_details (dict): A dictionary of tokens for the new account.

    Returns:
        str: Success message with the new account ID.
    """
    user_id = f"user{len(accounts_db) + 1}"
    accounts_db[user_id] = account_details
    return f"Account created with ID: {user_id}"

def delete_account(user_id):
    """
    Deletes a user account.

    Args:
        user_id (str): The ID of the account to delete.

    Returns:
        str: Success message if deleted, otherwise an error message.
    """
    if user_id in accounts_db:
        del accounts_db[user_id]
        return f"Account {user_id} deleted."
    else:
        return "Account not found."

# Example usage
accounts_db["user1"] = {
    "id_number": Token("id_number", "1", 0, 0),
    "name": Token("name", "John", 0, 1),
    "surname": Token("surname", "Doe", 0, 1),
    "password": Token("password", "password123", 0, 0),
    "amount_of_tokens": Token("amount_of_tokens", 100, 0, 2),
    "role": Token("role", "admin", 0, 0),
    "access_level": Token("access_level", 0, 0, 0)
}

accounts_db["user2"] = {
    "id_number": Token("id_number", "2", 1, 1),
    "name": Token("name", "Jane", 1, 1),
    "surname": Token("surname", "Smith", 1, 1),
    "password": Token("password", "mypassword", 1, 1),
    "amount_of_tokens": Token("amount_of_tokens", 150, 1, 2),
    "role": Token("role", "editor", 1, 1),
    "access_level": Token("access_level", 1, 1, 1)
}
