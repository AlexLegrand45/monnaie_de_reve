from database import Token, accounts_db

# Dictionary to store groups and their variables
groups_db = {}

class Group:
    """
    Represents a group with members and variables.

    Attributes:
        name (str): The name of the group.
        members (list): List of user IDs who are members of the group.
        variables (dict): Dictionary of group variables.
    """
    def __init__(self, name):
        self.name = name
        self.members = []
        self.variables = {}

    def add_member(self, user_id):
        """
        Adds a member to the group.

        Args:
            user_id (str): The ID of the user to add.
        """
        if user_id not in self.members:
            self.members.append(user_id)

    def remove_member(self, user_id):
        """
        Removes a member from the group.

        Args:
            user_id (str): The ID of the user to remove.
        """
        if user_id in self.members:
            self.members.remove(user_id)

    def add_variable(self, name, value, read_level, write_level):
        """
        Adds a variable to the group.

        Args:
            name (str): The name of the variable.
            value: The value of the variable.
            read_level (int): The minimum level required to read this variable.
            write_level (int): The minimum level required to write this variable.
        """
        self.variables[name] = Token(name, value, read_level, write_level, 0, 0)

    def remove_variable(self, name):
        """
        Removes a variable from the group.

        Args:
            name (str): The name of the variable to remove.
        """
        if name in self.variables:
            del self.variables[name]

def create_group(name):
    """
    Creates a new group.

    Args:
        name (str): The name of the group.

    Returns:
        str: Success message if created, otherwise an error message.
    """
    global groups_db
    if name not in groups_db:
        groups_db[name] = Group(name)
        return f"Group '{name}' created successfully."
    return f"Group '{name}' already exists."

def delete_group(name):
    """
    Deletes a group.

    Args:
        name (str): The name of the group to delete.

    Returns:
        str: Success message if deleted, otherwise an error message.
    """
    global groups_db
    if name in groups_db:
        del groups_db[name]
        return f"Group '{name}' deleted successfully."
    return f"Group '{name}' not found."

def add_member_to_group(group_name, user_id):
    """
    Adds a member to a group.

    Args:
        group_name (str): The name of the group.
        user_id (str): The ID of the user to add.

    Returns:
        str: Success message if added, otherwise an error message.
    """
    group = groups_db.get(group_name)
    if group:
        if user_id in accounts_db:
            group.add_member(user_id)
            return f"User '{user_id}' added to group '{group_name}' successfully."
        return f"User '{user_id}' not found."
    return f"Group '{group_name}' not found."

def remove_member_from_group(group_name, user_id):
    """
    Removes a member from a group.

    Args:
        group_name (str): The name of the group.
        user_id (str): The ID of the user to remove.

    Returns:
        str: Success message if removed, otherwise an error message.
    """
    group = groups_db.get(group_name)
    if group:
        group.remove_member(user_id)
        return f"User '{user_id}' removed from group '{group_name}' successfully."
    return f"Group '{group_name}' not found."

def create_group_variable(group_name, name, value, read_level, write_level):
    """
    Creates a new variable in a group.

    Args:
        group_name (str): The name of the group.
        name (str): The name of the variable.
        value: The value of the variable.
        read_level (int): The minimum level required to read this variable.
        write_level (int): The minimum level required to write this variable.

    Returns:
        str: Success message if created, otherwise an error message.
    """
    group = groups_db.get(group_name)
    if group:
        group.add_variable(name, value, read_level, write_level)
        return f"Variable '{name}' created in group '{group_name}' successfully."
    return f"Group '{group_name}' not found."

def delete_group_variable(group_name, name):
    """
    Deletes a variable from a group.

    Args:
        group_name (str): The name of the group.
        name (str): The name of the variable to delete.

    Returns:
        str: Success message if deleted, otherwise an error message.
    """
    group = groups_db.get(group_name)
    if group:
        group.remove_variable(name)
        return f"Variable '{name}' deleted from group '{group_name}' successfully."
    return f"Group '{group_name}' not found."

def get_group_variable(group_name, name, user_read_level):
    """
    Retrieves the value of a group variable if the user has sufficient read level.

    Args:
        group_name (str): The name of the group.
        name (str): The name of the variable to retrieve.
        user_read_level (int): The read level of the user.

    Returns:
        The variable's value if access is granted, otherwise an error message.
    """
    group = groups_db.get(group_name)
    if group:
        variable = group.variables.get(name)
        if variable and user_read_level <= variable.read_level:
            return variable.value
    return "Access denied or variable not found."

def update_group_variable(group_name, name, new_value, user_write_level):
    """
    Updates a group variable's value if the user has sufficient write level.

    Args:
        group_name (str): The name of the group.
        name (str): The name of the variable to update.
        new_value: The new value to set.
        user_write_level (int): The write level of the user.

    Returns:
        str: Success message if updated, otherwise an error message.
    """
    group = groups_db.get(group_name)
    if group:
        variable = group.variables.get(name)
        if variable and user_write_level <= variable.write_level:
            variable.value = new_value
            return f"Variable '{name}' in group '{group_name}' updated successfully."
    return "Access denied or variable not found."

def list_group_variables(group_name, user_read_level):
    """
    Lists all group variables that the user has permission to read.

    Args:
        group_name (str): The name of the group.
        user_read_level (int): The read level of the user.

    Returns:
        str: A formatted string containing all accessible variables.
    """
    group = groups_db.get(group_name)
    if group:
        accessible_vars = []
        for var_name, variable in group.variables.items():
            if user_read_level <= variable.read_level:
                accessible_vars.append(f"{var_name}: {variable}")

        if not accessible_vars:
            return f"No accessible variables found in group '{group_name}'."

        return f"Group '{group_name}' Variables:\n" + "\n".join(accessible_vars)
    return f"Group '{group_name}' not found."

def list_group_members(group_name):
    """
    Lists all members of a group.

    Args:
        group_name (str): The name of the group.

    Returns:
        str: A formatted string containing all members.
    """
    group = groups_db.get(group_name)
    if group:
        if not group.members:
            return f"No members found in group '{group_name}'."

        return f"Group '{group_name}' Members:\n" + "\n".join(group.members)
    return f"Group '{group_name}' not found."




def use_exemple():

    from groups import (
        create_group, delete_group,
        add_member_to_group, remove_member_from_group,
        create_group_variable, delete_group_variable,
        get_group_variable, update_group_variable,
        list_group_variables, list_group_members
    )

    # Create a group
    print(create_group("admins"))

    # Add members to the group
    print(add_member_to_group("admins", "user1"))
    print(add_member_to_group("admins", "user2"))

    # Create a group variable
    print(create_group_variable("admins", "max_members", 10, 1, 0))

    # Get a group variable
    print(get_group_variable("admins", "max_members", user_read_level=1))

    # Update a group variable
    print(update_group_variable("admins", "max_members", 15, user_write_level=0))

    # List group variables
    print(list_group_variables("admins", user_read_level=1))

    # List group members
    print(list_group_members("admins"))

    # Delete a group variable
    print(delete_group_variable("admins", "max_members"))

    # Delete a group
    print(delete_group("admins"))
