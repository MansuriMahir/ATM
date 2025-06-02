import random

ADMIN_ACCOUNT = "admin"
ADMIN_PIN = "1234"

user_accounts = {
    "1001": {"account_number": "1001", "pin": 1234, "balance": 1000, "full_name": "John Doe", "address": "123 Main St", "blood_group": "O+",
             "history": ["Inital Balance: 1000"]},
    "1002": {"account_number": "1002", "pin": 4321, "balance": 1500, "full_name": "Jane Smith", "address": "456 Oak Ave", "blood_group": "A-",
             "history": ["Inital Balance: 1500"]},
    "1003": {"account_number": "1003", "pin": 1111, "balance": 500, "full_name": "Peter Jones", "address": "789 Pine Ln", "blood_group": "B+",
             "history": ["Inital Balance: 500"]},
    "3001": {"account_number": "3001", "pin": 3001, "balance": 100, "full_name": "Alice Brown", "address": "101 Elm Rd", "blood_group": "AB-",
             "history": ["Inital Balance: 100"]}
}

def my_decorator(function):
    def wrapper(*args, **kwargs):
        print(f"\n--- {function.__name__.replace('_', ' ')} ---")
        result = function(*args, **kwargs)
        return result
    return wrapper

def generate_otp():
    """Generate a random 6-digit OTP code."""
    return str(random.randint(100000, 999999))
