import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk  # pip install pillow
import sys
import os
import random
import sqlite3

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define user dictionary
user = {}

# Import ATM classes and functions
from atm_utils import ADMIN_ACCOUNT, ADMIN_PIN, generate_otp
from Atm import ATM, Admin
from atm_utils import get_user

class ATMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ATM Machine")
        self.geometry("600x400")
        self.configure(bg="#b3d1ff")  # Light blue background

        # Set background gradient (simulate with a solid color for simplicity)
        # For a real gradient, use a Canvas and draw rectangles or use a gradient image
        # Optionally, you can use a background image as before
        try:
            bg_image = Image.open("background.jpg")
            bg_image = bg_image.resize((600, 400))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            pass  # If no image, just use background color

        # Style
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton",
                        font=("Consolas", 12, "bold"),
                        padding=10,
                        background="#1565c0",  # Navy blue
                        foreground="#ffffff",
                        borderwidth=0,
                        focusthickness=3,
                        focuscolor="#1565c0")
        style.map("TButton",
                  background=[('active', '#1976d2')],  # Lighter blue on hover
                  foreground=[('active', '#ffffff')])
        style.configure("TLabel",
                        font=("Consolas", 14),
                        background="#b3d1ff",
                        foreground="#1565c0")
        style.configure("Header.TLabel",
                        font=("Consolas", 20, "bold"),
                        background="#b3d1ff",
                        foreground="#0d1333")

        # Main frame (centered, semi-transparent)
        self.main_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="ridge")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=320)

        # Load user data from the database
        conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "atm-machine-api", "atm.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()

        for user_data in users:
            account_number = user_data[0]
            pin = user_data[1]
            balance = user_data[2]
            full_name = user_data[3]
            address = user_data[4]
            blood_group = user_data[5]
            user[account_number] = ATM(account_number, pin, balance, full_name, address, blood_group)
        
        # Current user
        self.current_user = None
        self.admin = None
        
        # Show main menu
        self.show_main_menu()
    
    def clear_frame(self):
        """Clear all widgets from the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        """Display the main menu"""
        self.clear_frame()
        
        # Header
        header = ttk.Label(self.main_frame, text="Welcome to ATM Machine", style="Header.TLabel")
        header.pack(pady=(30, 20))
        
        # Main menu buttons
        buttons = [
            ("Login as Admin", self.admin_login),
            ("Login to Existing Account", self.user_login),
            ("Create New Account", self.create_account)

        ]
        
        for text, command in buttons:
            btn = ttk.Button(self.main_frame, text=text, command=command, width=30)
            btn.pack(fill='x', padx=60, pady=8)
        
        # Add Exit button at the bottom
        exit_btn = ttk.Button(self.main_frame, text="Exit", command=self.quit, width=30)
        exit_btn.pack(fill='x', padx=60, pady=(30, 8))

    def admin_login(self):
        """Handle admin login"""
        admin_account = simpledialog.askstring("Admin Login", "Enter Admin Account Name:")
        if not admin_account:
            return
            
        if admin_account == ADMIN_ACCOUNT:
            admin_pin = simpledialog.askstring("Admin Login", "Enter Admin PIN:")
            if not admin_pin:
                return
                
            self.admin = Admin(admin_account, admin_pin)
            if self.admin.authenticate(admin_pin):
                self.show_admin_panel()
            else:
                messagebox.showerror("Error", "Invalid Admin PIN! Access denied.")
        else:
            messagebox.showerror("Error", "Invalid Admin account! Access denied.")
    
    def show_admin_panel(self):
        """Display the admin panel"""
        self.clear_frame()
        
        # Header
        header = ttk.Label(self.main_frame, text="Admin Panel", style="Header.TLabel")
        header.pack(pady=(0, 20))
        
        # Admin menu buttons
        buttons = [
            ("View All Users", self.admin_view_all_users),
            ("Delete User", self.admin_delete_user),
            ("Reset User PIN", self.admin_reset_pin),
            ("Reset User Balance", self.admin_reset_balance),
            ("Unblock User", self.admin_unblock_user),
            ("Edit User Details", self.admin_edit_user_details),
            ("View Total ATM Funds", self.admin_view_total_funds),
            ("Back to Main Menu", self.show_main_menu)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(self.main_frame, text=text, command=command, width=30)
            btn.pack(pady=5)
    
    def admin_view_all_users(self):
        """Display all users"""
        self.clear_frame()
        
        # Header
        header = ttk.Label(self.main_frame, text="All ATM Users", style="Header.TLabel")
        header.pack(pady=(0, 20))
        
        # Create a frame for the user list
        list_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create text widget for displaying users
        user_text = tk.Text(list_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, 
                           font=("Arial", 12), bg="#ffffff", height=15)
        user_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=user_text.yview)
        
        # Insert user information
        for acc_no, acc_obj in user.items():
            user_text.insert(tk.END, f"Account No : {acc_no}\n")
            user_text.insert(tk.END, f"Full Name  : {acc_obj.full_name}\n")
            user_text.insert(tk.END, f"Address    : {acc_obj.address}\n")
            user_text.insert(tk.END, f"Blood Group: {acc_obj.blood_group}\n")
            user_text.insert(tk.END, f"Balance    : {acc_obj.balance}\n")
            user_text.insert(tk.END, f"History    : {len(acc_obj.history) - 1} transaction(s)\n")
            user_text.insert(tk.END, f"Last Txn   : {acc_obj.history[-1]}\n")
            user_text.insert(tk.END, "-" * 30 + "\n\n")
        
        # Back button
        back_btn = ttk.Button(self.main_frame, text="Back to Admin Panel",
                             command=self.show_admin_panel)
        back_btn.pack(pady=10)
    
    def admin_delete_user(self):
        """Delete a user account"""
        acc_no = simpledialog.askstring("Delete User", "Enter account number to delete:")
        if not acc_no:
            return
            
        if acc_no in user:
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete account {acc_no}?")
            if confirm:
                self.admin.delete_user(acc_no)
                messagebox.showinfo("Success", f"Account {acc_no} deleted successfully.")
        else:
            messagebox.showerror("Error", "Account not found.")
    
    def admin_reset_pin(self):
        """Reset a user's PIN"""
        acc_no = simpledialog.askstring("Reset PIN", "Enter account number:")
        if not acc_no:
            return
            
        if acc_no in user:
            try:
                new_pin = simpledialog.askinteger("Reset PIN", "Enter new PIN:")
                if new_pin is not None:
                    self.admin.reset_pin(acc_no, new_pin)
                    messagebox.showinfo("Success", f"PIN for Account {acc_no} reset successfully.")
            except ValueError:
                messagebox.showerror("Error", "Invalid PIN format. Please enter a number.")
        else:
            messagebox.showerror("Error", "Account not found.")
    
    def admin_reset_balance(self):
        """Reset a user's balance"""
        acc_no = simpledialog.askstring("Reset Balance", "Enter account number:")
        if not acc_no:
            return
            
        if acc_no in user:
            try:
                new_balance = simpledialog.askfloat("Reset Balance", "Enter new balance:")
                if new_balance is not None:
                    self.admin.reset_balance(acc_no, new_balance)
                    messagebox.showinfo("Success", f"Balance for Account {acc_no} reset successfully.")
            except ValueError:
                messagebox.showerror("Error", "Invalid amount. Please enter a number.")
        else:
            messagebox.showerror("Error", "Account not found.")

    def admin_unblock_user(self):
        """Unblock a user account"""
        acc_no = simpledialog.askstring("Unblock User", "Enter account number to unblock:")
        if not acc_no:
            return

        if acc_no in user:
            user_atm = user[acc_no]
            user_atm.unblock()
            messagebox.showinfo("Success", f"Account {acc_no} unblocked successfully.")
        else:
            messagebox.showerror("Error", "Account not found.")
    
    def admin_view_total_funds(self):
        """View total funds in the ATM system"""
        total = sum(acc.balance for acc in user.values())
        messagebox.showinfo("Total Funds", f"Total money in ATM System: {total}")

    def admin_edit_user_details(self):
        """Edit user details"""
        acc_no = simpledialog.askstring("Edit User Details", "Enter account number to edit:")
        if not acc_no:
            return

        if acc_no in user:
            self.clear_frame()

            # Header
            header = ttk.Label(self.main_frame, text="Edit User Details", style="Header.TLabel")
            header.pack(pady=(0, 20))

            # Create form frame
            form_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
            form_frame.pack(fill=tk.BOTH, expand=True)

            # Get current user data
            current_user = user[acc_no]

            # Full Name
            ttk.Label(form_frame, text="Full Name:").pack(pady=5)
            full_name_var = tk.StringVar(value=current_user.full_name)
            full_name_entry = ttk.Entry(form_frame, textvariable=full_name_var, width=30)
            full_name_entry.pack(pady=5)

            # Address
            ttk.Label(form_frame, text="Address:").pack(pady=5)
            address_var = tk.StringVar(value=current_user.address)
            address_entry = ttk.Entry(form_frame, textvariable=address_var, width=30)
            address_entry.pack(pady=5)

            # Blood Group
            ttk.Label(form_frame, text="Blood Group:").pack(pady=5)
            blood_group_var = tk.StringVar(value=current_user.blood_group)
            blood_group_entry = ttk.Entry(form_frame, textvariable=blood_group_var, width=30)
            blood_group_entry.pack(pady=5)

            def save_changes():
                try:
                    # Update user object
                    current_user.full_name = full_name_var.get()
                    current_user.address = address_var.get()
                    current_user.blood_group = blood_group_var.get()

                    # Update database
                    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "atm-machine-api", "atm.db"))
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET full_name = ?, address = ?, blood_group = ?
                        WHERE account_number = ?
                    """, (current_user.full_name, current_user.address, 
                         current_user.blood_group, acc_no))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Success", "User details updated successfully!")
                    self.show_admin_panel()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update user details: {str(e)}")

            # Save button
            save_btn = ttk.Button(form_frame, text="Save Changes", command=save_changes)
            save_btn.pack(pady=20)

            # Back button
            back_btn = ttk.Button(form_frame, text="Back to Admin Panel",
                                command=self.show_admin_panel)
            back_btn.pack(pady=10)
        else:
            messagebox.showerror("Error", "Account not found.")
    
    def user_login(self):
        """Handle user login"""
        account_number = simpledialog.askstring("User Login", "Enter your account number:")
        if not account_number:
            return
            
        if account_number in user:
            user_atm = user[account_number]

            if user_atm.blocked:
                messagebox.showerror("Error", "Account is blocked. Please contact administrator.")
                return

            attempt = 0
            while attempt < 3:
                try:
                    entered_pin = simpledialog.askinteger("User Login", "Enter your PIN:")
                    if entered_pin is None:
                        return

                    if user_atm.authenticate(entered_pin):
                        # Two-Factor Authentication (Optional)
                        otp = generate_otp()
                        messagebox.showinfo("OTP", f"Your OTP is: {otp}")
                        otp_entered = simpledialog.askstring("OTP Verification", "Enter the OTP from the message box:")

                        if otp_entered == otp:
                            self.current_user = user_atm
                            self.show_user_menu()
                            return
                        else:
                            messagebox.showerror("Error", "Invalid OTP! Please try again.")
                            
                    else:
                        messagebox.showerror("Error", "Invalid PIN! Please try again.")
                        attempt += 1
                except ValueError:
                    messagebox.showerror("Error", "Invalid PIN format.")

            # Block account after 3 failed attempts
            user_atm.blocked = True
            messagebox.showerror("Error", "Too many incorrect attempts. Account blocked.")
        else:
            messagebox.showerror("Error", "Account not found. Please try again.")
    
    def show_user_menu(self):
        """Display the user menu"""
        self.clear_frame()
        
        # Header
        header = ttk.Label(self.main_frame, text=f"Welcome, Account {self.current_user.account_number}", style="Header.TLabel")
        header.pack(pady=(0, 10))

        # Balance Label
        balance = self.current_user.get_balance()
        balance_label = ttk.Label(self.main_frame, text=f"Current Balance: {balance}", style="TLabel")
        balance_label.pack(pady=(0, 20))

        buttons = [
            ("Check Balance", self.check_balance),
            ("Withdraw Money", self.withdraw_money),
            ("Deposit Money", self.deposit_money),
            ("View Transaction History", self.show_transaction_history),
            ("Change PIN", self.change_pin),
            ("View/Update Details", self.view_update_details),
            ("Back to Main Menu", self.logout)
        ]

        for text, command in buttons:
            btn = ttk.Button(self.main_frame, text=text, command=command, width=30)
            btn.pack(pady=5)
    
    def check_balance(self):
        """Check user balance"""
        balance = self.current_user.get_balance()
        messagebox.showinfo(
            "Balance",
            f"Account Number: {self.current_user.account_number}\n"
            f"Full Name: {self.current_user.full_name}\n"
            f"Address: {self.current_user.address}\n"
            f"Blood Group: {self.current_user.blood_group}\n"
            f"Your balance: {balance}"
        )
    
    def view_update_details(self):
        """View and update user details"""
        self.clear_frame()

        # Header
        header = ttk.Label(self.main_frame, text="View/Update Details", style="Header.TLabel")
        header.pack(pady=(0, 20))

        # Create form frame
        form_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Full Name
        name_label = ttk.Label(form_frame, text="Full Name:", style="TLabel")
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        name_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        name_entry.insert(0, self.current_user.full_name)

        # Address
        address_label = ttk.Label(form_frame, text="Address:", style="TLabel")
        address_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        address_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30)
        address_entry.grid(row=1, column=1, padx=10, pady=10)
        address_entry.insert(0, self.current_user.address)

        # Blood Group
        blood_label = ttk.Label(form_frame, text="Blood Group:", style="TLabel")
        blood_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        blood_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30)
        blood_entry.grid(row=2, column=1, padx=10, pady=10)
        blood_entry.insert(0, self.current_user.blood_group)

        # Save changes function
        def save_changes():
            self.current_user.full_name = name_entry.get().strip()
            self.current_user.address = address_entry.get().strip()
            self.current_user.blood_group = blood_entry.get().strip()

            # Update user details in the database
            conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "atm-machine-api", "atm.db"))
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET full_name=?, address=?, blood_group=? WHERE account_number=?",
                           (self.current_user.full_name, self.current_user.address, self.current_user.blood_group, self.current_user.account_number))
            conn.commit()
            conn.close()

        # Buttons
        btn_frame = tk.Frame(form_frame, bg="#f0f0f0")
        btn_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        save_btn = ttk.Button(btn_frame, text="Save Changes", command=save_changes)
        save_btn.pack(side=tk.LEFT, padx=5)

        back_btn = ttk.Button(self.main_frame, text="Back to User Menu", command=self.show_user_menu)
        back_btn.pack(pady=10)
    
    def withdraw_money(self):
        """Withdraw money from account"""
        try:
            amount = simpledialog.askfloat("Withdraw", "Enter withdrawal amount:")
            if amount is None:
                return

            pin = simpledialog.askinteger("Withdraw", "Enter your PIN:")
            if pin is None:
                return

            if not self.current_user.authenticate(pin):
                messagebox.showerror("Error", "Incorrect PIN. Please try again.")
                return
                
            result = self.current_user.withdraw(amount)
            if result == "Withdrawal Successful!":
                balance = self.current_user.get_balance()
                messagebox.showinfo("Success", f"{result}\nYour balance: {balance}")
            else:
                messagebox.showerror("Error", result)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount or PIN. Please enter a number.")
    
    def deposit_money(self):
        """Deposit money to account"""
        try:
            amount = simpledialog.askfloat("Deposit", "Enter deposit amount:")
            if amount is None:
                return
                
            result = self.current_user.deposit(amount)
            balance = self.current_user.get_balance()
            messagebox.showinfo("Success", f"{result}\nYour balance: {balance}")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a number.")
    
    def show_transaction_history(self):
        """View transaction history"""
        self.clear_frame()

        # Header
        header = ttk.Label(self.main_frame, text="Transaction History", style="Header.TLabel")
        header.pack(pady=(0, 20))

        # Create a frame for the history
        history_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        history_frame.pack(fill=tk.BOTH, expand=True)

        # Create scrollbar
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create text widget for displaying history
        history_text = tk.Text(history_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
                              font=("Arial", 12), bg="#ffffff", height=10)
        history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=history_text.yview)

        # Insert history
        self.display_transaction_history()

        # Back button
        back_btn = ttk.Button(self.main_frame, text="Back to User Menu",
                             command=self.show_user_menu)
        back_btn.pack(pady=10)

    def display_transaction_history(self):
        history_window = tk.Toplevel(self.main_frame)
        history_window.title("Transaction History")
        history_window.geometry("400x300")

        self.history_text = tk.Text(history_window, wrap=tk.WORD)
        self.history_text.pack(expand=True, fill=tk.BOTH)
        for transaction in self.current_user.transaction_history:
            print(transaction)
            self.history_text.insert(tk.END, transaction + "\n")
    def change_pin(self):
        """Change user PIN"""
        current_pin = simpledialog.askinteger("Change PIN", "Enter your current PIN:")
        if current_pin is None:
            return

        if not self.current_user.authenticate(current_pin):
            messagebox.showerror("Error", "Invalid current PIN. Please try again.")
            return
            
        new_pin = simpledialog.askinteger("Change PIN", "Enter your new PIN:")
        if new_pin is None:
            return

        self.current_user.pin = new_pin

        # Update PIN in the database
        conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "atm-machine-api", "atm.db"))
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET pin=? WHERE account_number=?",
                       (new_pin, self.current_user.account_number))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "PIN changed successfully!")
    
    def logout(self):
        """Log out the current user"""
        self.current_user = None
        self.show_main_menu()
    
    def create_account(self):
        """Create a new account"""
        self.clear_frame()
        
        # Header
        header = ttk.Label(self.main_frame, text="Create New Account", style="Header.TLabel")
        header.pack(pady=(0, 20))
        
        # Create form frame
        form_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Account number
        acc_label = ttk.Label(form_frame, text="Account Number:", style="TLabel")
        acc_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        acc_entry = ttk.Entry(form_frame, font=("Arial", 12), width=20)
        acc_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # PIN
        pin_label = ttk.Label(form_frame, text="PIN (4 digits):", style="TLabel")
        pin_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        pin_entry = ttk.Entry(form_frame, font=("Arial", 12), width=20)
        pin_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Initial balance
        bal_label = ttk.Label(form_frame, text="Initial Balance:", style="TLabel")
        bal_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        bal_entry = ttk.Entry(form_frame, font=("Arial", 12), width=20)
        bal_entry.grid(row=2, column=1, padx=10, pady=10)

        # Full Name
        name_label = ttk.Label(form_frame, text="Full Name:", style="TLabel")
        name_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        name_entry = ttk.Entry(form_frame, font=("Arial", 12), width=20)
        name_entry.grid(row=3, column=1, padx=10, pady=10)

        # Address
        address_label = ttk.Label(form_frame, text="Address:", style="TLabel")
        address_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        address_entry = ttk.Entry(form_frame, font=("Arial", 12), width=20)
        address_entry.grid(row=4, column=1, padx=10, pady=10)

        # Blood Group
        blood_label = ttk.Label(form_frame, text="Blood Group:", style="TLabel")
        blood_label.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
        blood_entry = ttk.Entry(form_frame, font=("Arial", 12), width=20)
        blood_entry.grid(row=5, column=1, padx=10, pady=10)
        
        # Status message
        status_var = tk.StringVar()
        status_label = ttk.Label(form_frame, textvariable=status_var, foreground="red")
        status_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        
        # Create account function
        def do_create_account():
            new_acc = acc_entry.get().strip()
            if not new_acc:
                status_var.set("Account number cannot be empty.")
                return
                
            if new_acc in user:
                status_var.set("Account already exists. Try a different number.")
                return
            
            try:
                new_pin = int(pin_entry.get().strip())
                init_balance = float(bal_entry.get().strip())
                full_name = name_entry.get().strip()
                address = address_entry.get().strip()
                blood_group = blood_entry.get().strip()
                
                user[new_acc] = ATM(new_acc, new_pin, init_balance, full_name, address, blood_group)
                
                # Call create_user to store the user data in the database
                from atm_utils import create_user
                create_user(new_acc, new_pin, init_balance, full_name, address, blood_group)
                
                messagebox.showinfo("Success", f"Account created successfully! Account No: {new_acc}")
                self.show_main_menu()
            except ValueError:
                status_var.set("Invalid input! Please enter valid numbers.")
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg="#f0f0f0")
        btn_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        
        create_btn = ttk.Button(btn_frame, text="Create Account", command=do_create_account)
        create_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=self.show_main_menu)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def view_total_users(self):
        """View total number of users"""
        messagebox.showinfo("Total Users", f"Total Users in ATM System: {len(user)}")
    
    def view_user_list(self):
        """View list of users with details"""
        self.clear_frame()
        
        # Header
        header = ttk.Label(self.main_frame, text="Registered Users in ATM", style="Header.TLabel")
        header.pack(pady=(0, 20))
        
        # Create a frame for the user list
        list_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create text widget for displaying users
        user_text = tk.Text(list_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, 
                           font=("Arial", 12), bg="#ffffff", height=15)
        user_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=user_text.yview)
        
        # Insert user information
        if not user:
            user_text.insert(tk.END, "No users found in the system.")
        else:
            for acc_no, acc_obj in user.items():
                last_txn = acc_obj.history[-1] if len(acc_obj.history) > 1 else "No transactions yet"
                user_text.insert(tk.END, f"Account Number: {acc_no}\n")
                user_text.insert(tk.END, f"Balance       : {acc_obj.balance}\n")
                user_text.insert(tk.END, f"Transaction   : {len(acc_obj.history)-1}\n")
                user_text.insert(tk.END, f"Last Transaction: {last_txn}\n")
                user_text.insert(tk.END, "-" * 30 + "\n\n") 
        
        # Back button
        back_btn = ttk.Button(self.main_frame, text="Back to Main Menu", 
                             command=self.show_main_menu)
        back_btn.pack(pady=10)

if __name__ == "__main__":
    app = ATMApp()
    app.mainloop()
