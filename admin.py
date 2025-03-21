from user import User
from database import Database
from loan_system import LoanSystem
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
    
    def approve_loan(self, loan_id, approved=True):
        """Approve or reject a loan application"""
        # Create a LoanSystem instance
        loan_system = LoanSystem()
        
        # Get loan details first to show more information
        loan_details = loan_system.get_loan_details(loan_id)
        if not loan_details:
            print(f"\n❌ Loan with ID {loan_id} not found.\n")
            return False, f"Loan with ID {loan_id} not found"
        
        # Approve or reject the loan
        success, message = loan_system.approve_loan(self.user_id, loan_id, approved)
        
        if success:
            action = "approved" if approved else "rejected"
            farmer_id = loan_details["farmer_id"]
            amount = loan_details["amount"]
            print(f"\n✅ {message}\n")
            return True, f"Loan {action} for farmer {farmer_id} in the amount of ₱{amount}"
        else:
            print(f"\n❌ {message}\n")
            return False, message
            
    def view_all_loans(self, status=None):
        """View all loans in the system, optionally filtered by status"""
        loan_system = LoanSystem()
        
        # Get loans based on status
        if status:
            filtered_loans = Database.get_loans_by_status(loan_system.loans_file, status)
        else:
            filtered_loans = Database.read_from_csv(loan_system.loans_file)
        
        if not filtered_loans:
            status_msg = f" with status '{status}'" if status else ""
            print(f"\n❌ No loans{status_msg} found.\n")
            return []
        
        print("\n===== Loan Applications =====\n")
        for loan in filtered_loans:
            if len(loan) >= 1:  # Ensure there's at least a loan ID
                loan_id = loan[0]
                farmer_id = loan[1] if len(loan) > 1 else "Unknown"
                amount = loan[2] if len(loan) > 2 else "Unknown"
                interest_rate = loan[3] if len(loan) > 3 else "Unknown"
                application_date = loan[4] if len(loan) > 4 else "Unknown"
                status = loan[5] if len(loan) > 5 else "Unknown"
                
                print(f"Loan ID: {loan_id}")
                print(f"Farmer ID: {farmer_id}")
                print(f"Amount: ₱{amount}")
                print(f"Interest Rate: {interest_rate}%")
                print(f"Application Date: {application_date}")
                print(f"Status: {status}")
                
                # If loan is approved, show approval date and due date
                if status == "Approved" and len(loan) >= 8:
                    approval_date = loan[6] if len(loan) > 6 else "Unknown"
                    due_date = loan[7] if len(loan) > 7 else "Unknown"
                    print(f"Approval Date: {approval_date}")
                    print(f"Due Date: {due_date}")
                
                print("\n----------------------------\n")
        
        return filtered_loans
    
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
            # Use the LoanSystem to generate a loan report
            loan_system = LoanSystem()
            report = loan_system.generate_loan_report()
            
            print("\n📊 Loan Report:")
            print(f"- Total Loans: {report['total_loans']}")
            print(f"- Pending Loans: {report['pending_loans']}")
            print(f"- Approved Loans: {report['approved_loans']}")
            print(f"- Rejected Loans: {report['rejected_loans']}")
            print(f"- Total Approved Amount: ₱{report['total_approved_amount']:.2f}")
            
            return True, report
        
        return False, f"Unknown report type: {report_type}"
