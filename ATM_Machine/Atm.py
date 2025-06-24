# creating ATM Machine

import datetime

from atm_utils import my_decorator, create_user, get_admin, get_user, update_user_balance, get_db_connection

class ATM:
    def __init__(self, account_number, pin, balance, full_name, address, blood_group, history=None):
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
        self.full_name = full_name
        self.address = address
        self.blood_group = blood_group 
        from atm_utils import get_transaction_history
        self.history = [f"Initial Balance: {balance}"]
        transactions = get_transaction_history(self.account_number)
        for transaction in transactions:
            self.history.append(f"{transaction['transaction_type']}: {transaction['amount']} | New Balance: {self.balance}")
        self.blocked = False
        self.transaction_history = []
    
    def authenticate(self, entered_pin):
        return self.pin == entered_pin

    def unblock(self):
        """Unblock the account"""
        self.blocked = False
    
    @my_decorator
    def get_balance(self):
        balance = self.balance
        return balance
    
    @my_decorator
    def withdraw(self, amount):
        if self.balance - amount < 0:
            return "Withdrawal failed: Insufficient balance."
        
        self.balance -= amount
        if self.balance == 100:
            return "Withdrawal Successful! Your balance is now 100."
        
        self.history.append(f"Withdrew: -{amount} | New Balance: {self.balance} ")
        update_user_balance(self.account_number, self.balance)
        get_db_connection().commit()
        from atm_utils import record_transaction
        record_transaction(self.account_number, "Withdrawal", amount)
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append(f"{timestamp} - Withdrawal: -{amount} | New Balance: {self.balance}")
        return "Withdrawal Successful!"
    
    @my_decorator
    def deposit(self, amount):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        self.balance += amount
        self.history.append(f"Deposit: +{amount} | New Balance: {self.balance}")
        update_user_balance(self.account_number, self.balance)
        get_db_connection().commit()
        from atm_utils import record_transaction
        record_transaction(self.account_number, "Deposit", amount)
        self.transaction_history.append(f"{timestamp} - Deposit: +{amount} | New Balance: {self.balance}")
        return "Deposit Successful!"
    
    @my_decorator
    def view_history(self):
        return "\n".join(self.transaction_history)


class Admin:
    def __init__(self, username, entered_pin):
        admin_data = get_admin(username)
        if admin_data:
            self.username = admin_data['username']
            self.pin = admin_data['pin']
        else:
            self.username = username
            self.pin = entered_pin

    def authenticate(self, entered_pin):
        if self.pin is not None:
            return str(self.pin) == str(entered_pin)
        return False

    @my_decorator
    def view_all_users(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()

        print("\n--- All ATM Users ---")
        for user in users:
            print(f"Account No : {user['account_number']}")
            print(f"Full Name  : {user['full_name']}")
            print(f"Address    : {user['address']}")
            print(f"Blood Group: {user['blood_group']}")
            print(f"Balance    : {user['balance']}")
            #print(f"History    : {len(acc_obj.history) - 1} transaction(s)") # Transaction history not implemented yet
            #print(f"Last Txn   : {acc_obj.history[-1]}")
            print("-" * 30)

    @my_decorator
    def delete_user(self, acc_no):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE account_number = ?", (acc_no,))
        conn.commit()
        conn.close()
        print(f"Account {acc_no} deleted successfully.")

    @my_decorator
    def reset_pin(self, acc_no, new_pin):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET pin = ? WHERE account_number = ?", (new_pin, acc_no))
        conn.commit()
        conn.close()
        print(f"PIN for Account {acc_no} reset successfully.")

    @my_decorator
    def reset_balance(self, acc_no, new_balance):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = ? WHERE account_number = ?", (new_balance, acc_no))
        conn.commit()
        conn.close()
        print(f"Balance for Account {acc_no} reset successfully.")

    @my_decorator
    def view_total_funds(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(balance) FROM users")
        total = cursor.fetchone()[0]
        conn.close()
        print(f"Total money in ATM System: {total}")

@my_decorator   
def make_choice(atm: ATM):
     while True:
        print("\nATM Menu:")
        print("1. Check Balance")
        print("2. Withdraw Money")
        print("3. Deposit Money")
        print("4. View Balance History")
        print("5. Exit \n")
    
        choice = input("Enter your choice: ")

        if choice == "1":
            balance = atm.get_balance()
            print(f"Account Number: {atm.account_number}")
            print(f"Full Name: {atm.full_name}")
            print(f"Address: {atm.address}")
            print(f"Blood Group: {atm.blood_group}")
            print(f"Your balance : {balance}")
    
        elif choice == "2":
            try:
                amount = float(input("Enter withdrawal amount: "))
                print(atm.withdraw(amount))
                balance = atm.get_balance()
                print(f'Your balance : {balance}')
            except ValueError:
                print("Invalid amount. Please enter a number")
    
        elif choice == "3":
            try:
                amount = float(input("Enter deposit amount :"))
                print(atm.deposit(amount))
                balance = atm.get_balance()
                print(f'your balance : {balance}')
            except ValueError:
                print("Invalid amount. Please enter a number")

        elif choice == "4":
            print(atm.view_history())
    
        elif choice == "5":
            print("thank you for using the ATM")
            return # Changed break to return
        else:
            print("Invalid choice. Please try again. ")


@my_decorator
def show_user_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    if not users:
        print("No user found in the system.")
        return

    print("\n--- Registered User in ATM ---")
    for user in users:
        print(f"Account Number: {user['account_number']}")
        print(f"Balance       : {user['balance']}")
        #print(f"Transaction   : {len(acc_obj.history)-1} ") # Transaction history not implemented yet
        #print(f"Last Transaction: {last_txn}")
        print("-" * 30)

def create_account():
    print("\n--- Create New Account ---")
    while True:
        new_acc = input("Enter new Account Number: ")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE account_number = ?", (new_acc,))
        existing_user = cursor.fetchone()
        conn.close()
        if existing_user:
            print("Account already exists. Try a different number.")
        else:
            break

    try:
        new_pin = int(input("Set a 4-digit PIN: "))
        init_balance = float(input("Enter initial deposit amount: "))
        full_name = input("Enter your full name: ")
        address = input("Enter your address: ")
        blood_group = input("Enter your blood group: ")
    except ValueError:
        print("Invalid input! Account creation failed")
        return

    create_user(new_acc, new_pin, init_balance, full_name, address, blood_group)
    print(f"Account created successfully! Account No:{new_acc}")

def handle_admin_panel(admin):
    while True:
        print("\n--- Admin Panel ---")
        print("1. View All Users")
        print("2. Delete User")
        print("3. Reset User PIN")
        print("4. Reset User Balance")
        print("5. View Total ATM Funds")
        print("6. Exit Admin Panel")

        admin_choice = input("Enter your Choice: ")

        if admin_choice == "1":
            admin.view_all_users()

        elif admin_choice == "2":
            acc_no = input("Enter account number to delete: ")
            admin.delete_user(acc_no)

        elif admin_choice == "3":
            acc_no = input("Enter account number to reset PIN: ")
            try:
                new_pin = int(input("Enter new PIN: "))
                admin.reset_pin(acc_no, new_pin)
            except ValueError:
                print("Invalid PIN. Please enter a number.")

# Test functions
def test_create_user():
    create_user("4001", 1234, 1000, "Test User", "Test Address", "O+")
    print("User created successfully!")

def test_get_user():
    user = get_user("4001")
    if user:
        print(f"User found: {user['full_name']}")
    else:
        print("User not found.")

def test_update_balance():
    update_user_balance("4001", 2000)
    print("Balance updated successfully!")

# test_create_user()
# test_get_user()
# test_update_balance()
