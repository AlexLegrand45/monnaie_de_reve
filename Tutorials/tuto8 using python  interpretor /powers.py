import threading
import time
from database import accounts_db

# Dictionary to store powers
powers_db = {}

# Dictionary to store scheduled powers and their threads
scheduled_powers = {}

class Power:
    """
    Represents a Python power with execution permissions and scheduling options.

    Attributes:
        name (str): The name of the power.
        code (str): The Python code of the power.
        call_level (int): The minimum level required to call this power.
        schedule_interval (int): The interval in seconds for scheduled execution (0 for non-scheduled powers).
        thread (threading.Thread): The thread for scheduled execution.
        stop_event (threading.Event): Event to stop the scheduled execution.
    """
    def __init__(self, name, code, call_level, schedule_interval=0):
        self.name = name
        self.code = code
        self.call_level = call_level
        self.schedule_interval = schedule_interval
        self.thread = None
        self.stop_event = threading.Event()

    def execute(self):
        """
        Executes the power's code.
        """
        try:
            exec(self.code, globals())
        except Exception as e:
            print(f"Error executing power '{self.name}': {e}")

    def start_schedule(self):
        """
        Starts the scheduled execution of the power in a separate thread.
        """
        if self.schedule_interval > 0:
            self.stop_event.clear()
            self.thread = threading.Thread(target=self._schedule_loop)
            self.thread.start()

    def stop_schedule(self):
        """
        Stops the scheduled execution of the power.
        """
        if self.thread and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join()

    def _schedule_loop(self):
        """
        Loop for scheduled execution of the power.
        """
        while not self.stop_event.is_set():
            self.execute()
            time.sleep(self.schedule_interval)

def create_power(name, code, call_level, schedule_interval=0):
    """
    Creates a new power.

    Args:
        name (str): The name of the power.
        code (str): The Python code of the power.
        call_level (int): The minimum level required to call this power.
        schedule_interval (int): The interval in seconds for scheduled execution (0 for non-scheduled powers).

    Returns:
        str: Success message if created, otherwise an error message.
    """
    global powers_db
    if name not in powers_db:
        powers_db[name] = Power(name, code, call_level, schedule_interval)
        if schedule_interval > 0:
            scheduled_powers[name] = powers_db[name]
            powers_db[name].start_schedule()
        return f"Power '{name}' created successfully."
    return f"Power '{name}' already exists."

def delete_power(name):
    """
    Deletes a power.

    Args:
        name (str): The name of the power to delete.

    Returns:
        str: Success message if deleted, otherwise an error message.
    """
    global powers_db, scheduled_powers
    if name in powers_db:
        if name in scheduled_powers:
            powers_db[name].stop_schedule()
            del scheduled_powers[name]
        del powers_db[name]
        return f"Power '{name}' deleted successfully."
    return f"Power '{name}' not found."

def call_power(name, user_call_level):
    """
    Calls a power if the user has sufficient level.

    Args:
        name (str): The name of the power to call.
        user_call_level (int): The level of the user calling the power.

    Returns:
        str: Success message if called, otherwise an error message.
    """
    power = powers_db.get(name)
    if power and user_call_level <= power.call_level:
        power.execute()
        return f"Power '{name}' executed successfully."
    return "Access denied or power not found."

def list_powers(user_call_level):
    """
    Lists all powers that the user has permission to call.

    Args:
        user_call_level (int): The level of the user.

    Returns:
        str: A formatted string containing all accessible powers.
    """
    accessible_powers = []
    for power_name, power in powers_db.items():
        if user_call_level <= power.call_level:
            accessible_powers.append(f"{power_name} (call level: {power.call_level})")

    if not accessible_powers:
        return "No accessible powers found."

    return "Powers:\n" + "\n".join(accessible_powers)

def stop_all_scheduled_powers():
    """
    Stops all scheduled powers.

    Returns:
        str: Success message.
    """
    global scheduled_powers
    for power_name, power in scheduled_powers.items():
        power.stop_schedule()
    scheduled_powers.clear()
    return "All scheduled powers stopped successfully."



def use_exemple():
    from powers import create_power, delete_power, call_power, list_powers, stop_all_scheduled_powers

    # Create a power that can be called by users with level <= 1
    power_code = """
    print("Hello, this is a test power!")
    """
    print(create_power("test_power", power_code, call_level=1))

    # Call the power with a user who has sufficient level
    print(call_power("test_power", user_call_level=1))

    # Create a scheduled power that runs every 5 seconds
    scheduled_power_code = """
    print("This scheduled power is running!")
    """
    print(create_power("scheduled_power", scheduled_power_code, call_level=0, schedule_interval=5))

    # List all accessible powers
    print(list_powers(user_call_level=1))

    # Delete a power
    print(delete_power("test_power"))

    # Stop all scheduled powers
    print(stop_all_scheduled_powers())
