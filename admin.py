from user import User
from database import Database
import csv
import os

class Admin(User):
    def __init__(self, name, user_id=None, email=None, password=None):
        # Call the parent class constructor
        super().__init__(user_id=user_id, name=name, email=email, password=password, role="admin")
        self.admin_id = self.user_id
        self.role = "admin"

    def approve_transaction(self, buyer_name, product_name):
        """Approve a transaction between a buyer and seller"""
        print(f"\n🔍 Admin {self.name} is approving {buyer_name}'s purchase of {product_name}...\n")
        
        # Get transactions from CSV
        transactions_file = os.path.join("data", "transactions.csv")
        if not os.path.isfile(transactions_file):
            print("\n❌ No transactions found.\n")
            return False, "No transactions found"
        
        with open(transactions_file, mode='r') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Skip header row
            transactions = list(reader)
        
        # Find and update the transaction
        updated_transactions = []
        found = False
        
        for transaction in transactions:
            # Check if this is the transaction we're looking for
            if len(transaction) >= 3 and transaction[1] == buyer_name and transaction[2] == product_name and transaction[4] == "Pending":
                transaction[4] = "Approved"  # Update status
                found = True
                print(f"\n✅ Transaction approved: {buyer_name}'s purchase of {product_name}\n")
            updated_transactions.append(transaction)
        
        if not found:
            print("\n❌ Transaction not found or already approved.\n")
            return False, "Transaction not found or already approved"
        
        # Write updated transactions back to CSV
        with open(transactions_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(updated_transactions)
        
        return True, f"Transaction approved: {buyer_name}'s purchase of {product_name}"
    
    def approve_loan(self, farmer_id, loan_amount):
        """Approve a loan application from a farmer"""
        loans_file = os.path.join("data", "loans.csv")
        if not os.path.isfile(loans_file):
            print("\n❌ No loan applications found.\n")
            return False, "No loan applications found"
        
        with open(loans_file, mode='r') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Skip header row
            loans = list(reader)
        
        # Find and update the loan
        updated_loans = []
        found = False
        
        for loan in loans:
            # Check if this is the loan we're looking for
            if len(loan) >= 3 and loan[0] == farmer_id and float(loan[2]) == float(loan_amount) and loan[4] == "Pending":
                loan[4] = "Approved"  # Update status
                found = True
                print(f"\n✅ Loan approved: {loan[1]}'s loan for ₱{loan_amount}\n")
            updated_loans.append(loan)
        
        if not found:
            print("\n❌ Loan not found or already approved.\n")
            return False, "Loan not found or already approved"
        
        # Write updated loans back to CSV
        with open(loans_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(updated_loans)
        
        return True, f"Loan approved for farmer {farmer_id} in the amount of ₱{loan_amount}"
    
    def manage_users(self, action, user_id=None, new_data=None):
        """Manage users in the system (view, update, delete)"""
        users = Database.read_from_csv(self.users_file)
        
        if action == "view":
            if not users:
                return False, "No users found"
            
            print("\n👥 User List:")
            for user in users:
                print(f"- ID: {user[0]} | Username: {user[1]} | Role: {user[3]} | Email: {user[4]}")
            return True, users
            
        elif action == "delete" and user_id:
            updated_users = []
            found = False
            
            for user in users:
                if user[0] != user_id:
                    updated_users.append(user)
                else:
                    found = True
            
            if not found:
                return False, f"User with ID {user_id} not found"
            
            # Write updated users back to CSV
            with open(f"data/{self.users_file}", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
                writer.writerows(updated_users)
            
            return True, f"User with ID {user_id} deleted successfully"
        
        return False, "Invalid action or missing user ID"
    
    def generate_report(self, report_type):
        """Generate various reports for the system"""
        if report_type == "transactions":
            transactions = Database.read_from_csv("transactions.csv")
            if not transactions:
                return False, "No transactions found"
            
            # Count transactions by status
            pending = sum(1 for t in transactions if t[4] == "Pending")
            approved = sum(1 for t in transactions if t[4] == "Approved")
            
            # Calculate total value
            total_value = sum(float(t[3]) for t in transactions if len(t) > 3)
            
            report = {
                "total_transactions": len(transactions),
                "pending": pending,
                "approved": approved,
                "total_value": total_value
            }
            
            print("\n📊 Transaction Report:")
            print(f"- Total Transactions: {report['total_transactions']}")
            print(f"- Pending: {report['pending']}")
            print(f"- Approved: {report['approved']}")
            print(f"- Total Value: ₱{report['total_value']:.2f}")
            
            return True, report
            
        elif report_type == "users":
            users = Database.read_from_csv(self.users_file)
            if not users:
                return False, "No users found"
            
            # Count users by role
            farmers = sum(1 for u in users if u[3] == "farmer")
            buyers = sum(1 for u in users if u[3] == "buyer")
            admins = sum(1 for u in users if u[3] == "admin")
            
            report = {
                "total_users": len(users),
                "farmers": farmers,
                "buyers": buyers,
                "admins": admins
            }
            
            print("\n📊 User Report:")
            print(f"- Total Users: {report['total_users']}")
            print(f"- Farmers: {report['farmers']}")
            print(f"- Buyers: {report['buyers']}")
            print(f"- Admins: {report['admins']}")
            
            return True, report
            
        elif report_type == "loans":
            loans = Database.read_from_csv("loans.csv")
            if not loans:
                return False, "No loans found"
            
            # Count loans by status
            pending = sum(1 for l in loans if l[4] == "Pending")
            approved = sum(1 for l in loans if l[4] == "Approved")
            
            # Calculate total value
            total_value = sum(float(l[2]) for l in loans if len(l) > 2)
            
            report = {
                "total_loans": len(loans),
                "pending": pending,
                "approved": approved,
                "total_value": total_value
            }
            
            print("\n📊 Loan Report:")
            print(f"- Total Loans: {report['total_loans']}")
            print(f"- Pending: {report['pending']}")
            print(f"- Approved: {report['approved']}")
            print(f"- Total Value: ₱{report['total_value']:.2f}")
            
            return True, report
        
        return False, f"Unknown report type: {report_type}"
