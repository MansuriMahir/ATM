# creating ATM Machine 

from atm_utils import my_decorator, user_accounts, ADMIN_ACCOUNT, ADMIN_PIN

class ATM:
    def __init__(self, account_number, pin, balance, full_name, address, blood_group, history=None):
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
        self.full_name = full_name
        self.address = address
        self.blood_group = blood_group
        self.history = history if history else [f"Inital Balance: {balance}"]
        self.blocked = False
    
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
        if self.balance >= amount:
            self.balance -= amount
            self.history.append(f"Withdrew: -{amount} | New Balance: {self.balance} ")
            return "Withdrawal Successful!"
        else:
            return "Insufficient Balance!"
    
    @my_decorator
    def deposit(self, amount):
        self.balance += amount
        self.history.append(f"Deposit: +{amount} | New Balance: {self.balance}")
        return "Deposit Successful!"
    
    @my_decorator
    def view_history(self):
        return "\n".join(self.history)

class Admin:
    def __init__(self, account, pin):
        self.account = account
        self.pin = pin

    def authenticate(self, entered_pin):
        return self.pin == entered_pin

    @my_decorator
    def view_all_users(self):
        print("\n--- All ATM Users ---")
        for acc_no, acc_obj in user.items():
            print(f"Account No : {acc_no}")
            print(f"Full Name  : {acc_obj.full_name}")
            print(f"Address    : {acc_obj.address}")
            print(f"Blood Group: {acc_obj.blood_group}")
            print(f"Balance    : {acc_obj.balance}")
            print(f"History    : {len(acc_obj.history) - 1} transaction(s)")
            print(f"Last Txn   : {acc_obj.history[-1]}")
            print("-" * 30)

    @my_decorator
    def delete_user(self, acc_no):
        if acc_no in user:
            del user[acc_no]
            print(f"Account {acc_no} deleted successfully.")
        else:
            print("Account not found.")

    @my_decorator
    def reset_pin(self, acc_no, new_pin):
        if acc_no in user:
            user[acc_no].pin = new_pin
            user[acc_no].history.append(f"PIN reset by Admin.")
            print(f"PIN for Account {acc_no} reset successfully.")
        else:
            print("Account not found.")

    @my_decorator
    def reset_balance(self, acc_no, new_balance):
        if acc_no in user:
            user[acc_no].balance = new_balance
            user[acc_no].history.append(f"Balance reset by Admin to {new_balance}")
            print(f"Balance for Account {acc_no} reset successfully.")
        else:
            print("Account not found.")

    @my_decorator
    def view_total_funds(self):
        total = sum(acc.balance for acc in user.values())
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
            pass
    
        elif choice == "5":
            print("thank you for using the ATM")
            break
        else:
            print("Invalid choice. Please try again. ")

# Initialize user dictionary from user_accounts data
user = {}
for acc_no, acc_data in user_accounts.items():
    user[acc_no] = ATM(
        acc_data["account_number"],
        acc_data["pin"],
        acc_data["balance"],
        acc_data["full_name"],
        acc_data["address"],
        acc_data["blood_group"],
        acc_data["history"]
    )

@my_decorator
def show_user_list():
    if not user:
        print("No user found in the system. ")
        return
    print("\n--- Registered User in ATM ---")
    for acc_no, acc_obj in user.items():
        last_txn = acc_obj.history[-1] if len(acc_obj.history) > 1 else "No transactions yet "
        print(f"Account Number: {acc_no}")
        print(f"Balance       : {acc_obj.balance}")
        print(f"Transaction   : {len(acc_obj.history)-1} ")
        print(f"Last Transaction: {last_txn}")
        print("-" * 30)

def create_account():
    print("\n--- Create New Account ---")
    while True:
        new_acc = input("Enter new Account Number: ")
        if new_acc in user:
            print("Account already exits. try a different number. ")
        else:
            break
    try:
        new_pin = int(input("Set a 4-digit PIN: "))
        init_balance = float(input("Enter inital deposit amount: "))
        full_name = input("Enter your full name: ")
        address = input("Enter your address: ")
        blood_group = input("Enter your blood group: ")
    except ValueError:
        print("Invalid input! Account creation failed")
        return
    
    user[new_acc] = ATM(new_acc, new_pin, init_balance, full_name, address, blood_group)
    print(f"Account created successfuly! Account No:{new_acc}")

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
