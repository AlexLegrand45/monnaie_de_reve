from database import Token

# Dictionary to store global variables
global_variables = {}

def create_variable(name, value, read_level, write_level):
    """
    Creates a new global variable.

    Args:
        name (str): The name of the variable.
        value: The value of the variable.
        read_level (int): The minimum level required to read this variable.
        write_level (int): The minimum level required to write this variable.

    Returns:
        str: Success message if created.
    """
    global global_variables
    global_variables[name] = Token(name, value, read_level, write_level, 0, 0)
    return f"Variable '{name}' created successfully."

def delete_variable(name):
    """
    Deletes a global variable.

    Args:
        name (str): The name of the variable to delete.

    Returns:
        str: Success message if deleted, otherwise an error message.
    """
    global global_variables
    if name in global_variables:
        del global_variables[name]
        return f"Variable '{name}' deleted successfully."
    return f"Variable '{name}' not found."

def get_variable(name, user_read_level):
    """
    Retrieves the value of a global variable if the user has sufficient read level.

    Args:
        name (str): The name of the variable to retrieve.
        user_read_level (int): The read level of the user.

    Returns:
        The variable's value if access is granted, otherwise an error message.
    """
    variable = global_variables.get(name)
    if variable and user_read_level <= variable.read_level:
        return variable.value
    return "Access denied or variable not found."

def update_variable(name, new_value, user_write_level):
    """
    Updates a global variable's value if the user has sufficient write level.

    Args:
        name (str): The name of the variable to update.
        new_value: The new value to set.
        user_write_level (int): The write level of the user.

    Returns:
        str: Success message if updated, otherwise an error message.
    """
    variable = global_variables.get(name)
    if variable and user_write_level <= variable.write_level:
        variable.value = new_value
        return f"Variable '{name}' updated successfully."
    return "Access denied or variable not found."

def list_variables(user_read_level):
    """
    Lists all global variables that the user has permission to read.

    Args:
        user_read_level (int): The read level of the user.

    Returns:
        str: A formatted string containing all accessible variables.
    """
    accessible_vars = []
    for var_name, variable in global_variables.items():
        if user_read_level <= variable.read_level:
            accessible_vars.append(f"{var_name}: {variable}")

    if not accessible_vars:
        return "No accessible variables found."

    return "Global Variables:\n" + "\n".join(accessible_vars)



def use_exemple():
    from variables import create_variable, get_variable, update_variable, delete_variable, list_variables

    # Assume user_read_level and user_write_level are determined elsewhere
    user_read_level = 1
    user_write_level = 0

    # Create a global variable
    print(create_variable("max_users", 100, 1, 0))

    # Get the value of a global variable
    print(get_variable("max_users", user_read_level))

    # Update the value of a global variable
    print(update_variable("max_users", 150, user_write_level))

    # List all accessible global variables
    print(list_variables(user_read_level))

    # Delete a global variable
    print(delete_variable("max_users"))
