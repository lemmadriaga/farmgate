from user import User
from database import Database
from loan_system import LoanSystem
from educational_hub import EducationalHub
import csv
import os

class Admin(User):
    def __init__(self, name, user_id=None, email=None, password=None):
        # Call the parent class constructor
        super().__init__(user_id=user_id, name=name, email=email, password=password, role="admin")
        self.admin_id = self.user_id
        self.role = "admin"

    def approve_transaction(self, transaction_id=None, buyer_name=None, product_name=None):
        """Approve a transaction between a buyer and seller with blockchain integration"""
        # Import transaction manager here to avoid circular imports
        from transactions import TransactionManager
        transaction_manager = TransactionManager()
        
        if transaction_id:
            # Use transaction ID for blockchain-based approval
            print(f"\n🔍 Admin {self.name} is approving transaction {transaction_id}...\n")
            
            # Approve transaction in the blockchain system
            success, message = transaction_manager.approve_transaction(transaction_id)
            
            if success:
                # Execute any associated smart contracts
                # Get all transactions to find the contract ID
                transactions = transaction_manager.get_transactions(show_output=False)
                contract_id = None
                
                # Find the contract ID for this transaction by checking blockchain records
                contracts = transaction_manager.blockchain.get_contract_history()
                for contract in contracts:
                    # Try to match by transaction ID in the future
                    # For now, we'll just execute the most recent contract
                    if contract["status"] == "Created":
                        contract_id = contract["contract_id"]
                        break
                
                # Execute the smart contract if found
                if contract_id:
                    transaction_manager.execute_smart_contract(contract_id)
                    print(f"\n Smart contract {contract_id} executed for transaction {transaction_id}\n")
                    return True, f"Transaction {transaction_id} approved and smart contract executed"
                
                return True, message
            return False, message
            
        elif buyer_name and product_name:
            # Legacy approval method using buyer name and product name
            print(f"\n🔍 Admin {self.name} is approving {buyer_name}'s purchase of {product_name}...\n")
            
            # Get transactions from CSV
            transactions_file = os.path.join("data", "transactions.csv")
            if not os.path.isfile(transactions_file):
                print("\n No transactions found.\n")
                return False, "No transactions found"
            
            with open(transactions_file, mode='r') as file:
                reader = csv.reader(file)
                headers = next(reader)  # Skip header row
                transactions = list(reader)
            
            # Find and update the transaction
            updated_transactions = []
            found = False
            found_transaction_id = None
            
            for transaction in transactions:
                # Check if this is the transaction we're looking for
                if len(transaction) >= 3 and transaction[1] == buyer_name and transaction[2] == product_name and transaction[4] == "Pending":
                    transaction[4] = "Approved"  # Update status
                    found = True
                    if len(transaction) >= 5:
                        found_transaction_id = transaction[4]
                    print(f"\n Transaction approved: {buyer_name}'s purchase of {product_name}\n")
                updated_transactions.append(transaction)
            
            if not found:
                print("\n Transaction not found or already approved.\n")
                return False, "Transaction not found or already approved"
            
            # Write updated transactions back to CSV
            with open(transactions_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(updated_transactions)
            
            # If we found a transaction ID, also update in blockchain
            if found_transaction_id:
                transaction_manager.approve_transaction(found_transaction_id)
            
            return True, f"Transaction approved: {buyer_name}'s purchase of {product_name}"
        else:
            print("\n Please provide either transaction_id or both buyer_name and product_name.\n")
            return False, "Missing required parameters"
    
    def approve_loan(self, loan_id, approved=True):
        """Approve or reject a loan application"""
        # Create a LoanSystem instance
        loan_system = LoanSystem()
        
        # Get loan details first to show more information
        loan_details = loan_system.get_loan_details(loan_id)
        if not loan_details:
            print(f"\n Loan with ID {loan_id} not found.\n")
            return False, f"Loan with ID {loan_id} not found"
        
        # Approve or reject the loan
        success, message = loan_system.approve_loan(self.user_id, loan_id, approved)
        
        if success:
            action = "approved" if approved else "rejected"
            farmer_id = loan_details["farmer_id"]
            amount = loan_details["amount"]
            print(f"\n {message}\n")
            return True, f"Loan {action} for farmer {farmer_id} in the amount of ₱{amount}"
        else:
            print(f"\n {message}\n")
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
            print(f"\n No loans{status_msg} found.\n")
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
            pending = sum(1 for t in transactions if len(t) > 3 and t[3] == "Pending")
            approved = sum(1 for t in transactions if len(t) > 3 and t[3] == "Approved")
            
            # Calculate total value
            total_value = sum(float(t[2]) for t in transactions if len(t) > 2 and t[2].replace('.', '', 1).isdigit())
            
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
            
            # Add blockchain transaction statistics
            from transactions import TransactionManager
            transaction_manager = TransactionManager()
            blockchain_transactions = transaction_manager.blockchain.get_transaction_history()
            
            blockchain_pending = sum(1 for tx in blockchain_transactions if tx["status"] == "Pending")
            blockchain_confirmed = sum(1 for tx in blockchain_transactions if tx["status"] == "Confirmed")
            blockchain_total = sum(tx["amount"] for tx in blockchain_transactions)
            
            print("\n📊 Blockchain Transaction Report:")
            print(f"- Total Blockchain Transactions: {len(blockchain_transactions)}")
            print(f"- Pending: {blockchain_pending}")
            print(f"- Confirmed: {blockchain_confirmed}")
            print(f"- Total Value: ₱{blockchain_total:.2f}")
            
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
        
        elif report_type == "education":
            # Generate a report on educational resources
            hub = EducationalHub()
            resources = Database.read_from_csv(hub.resources_file)
            
            # Count resources by category
            categories = {}
            for resource in resources:
                if len(resource) >= 3:
                    category = resource[2]
                    if category in categories:
                        categories[category] += 1
                    else:
                        categories[category] = 1
            
            report = {
                "total_resources": len(resources),
                "categories": categories
            }
            
            print("\n📊 Educational Resources Report:")
            print(f"- Total Resources: {report['total_resources']}")
            print("- Resources by Category:")
            for category, count in categories.items():
                print(f"  * {category}: {count}")
            
            return True, report
            
        return False, f"Unknown report type: {report_type}"
    
    # Educational Hub Management Methods
    def add_educational_resource(self, title, category, content, tags):
        """Add a new educational resource to the system."""
        hub = EducationalHub()
        success, message, resource_id = hub.add_resource(title, category, content, tags)
        
        if success:
            print(f"\n {message}\n")
        else:
            print(f"\n {message}\n")
            
        return success, message
    
    def delete_educational_resource(self, resource_id):
        """Delete an educational resource from the system."""
        # Get all resources
        hub = EducationalHub()
        resources = Database.read_from_csv(hub.resources_file)
        
        # Find and remove the resource
        updated_resources = []
        found = False
        
        for resource in resources:
            if len(resource) >= 1 and resource[0] == resource_id:
                found = True
                continue
            updated_resources.append(resource)
        
        if not found:
            print(f"\n Resource with ID '{resource_id}' not found.\n")
            return False, f"Resource with ID '{resource_id}' not found"
        
        # Write updated resources back to CSV
        Database.update_csv_file(hub.resources_file, updated_resources)
        
        print(f"\n Resource with ID '{resource_id}' deleted successfully.\n")
        return True, f"Resource with ID '{resource_id}' deleted successfully"
    
    def update_educational_resource(self, resource_id, title=None, category=None, content=None, tags=None):
        """Update an existing educational resource."""
        # Get all resources
        hub = EducationalHub()
        resources = Database.read_csv_with_headers(hub.resources_file)
        
        if not resources or len(resources) < 2:
            print("\n No resources found.\n")
            return False, "No resources found"
        
        # Find and update the resource
        headers = resources[0]
        updated_resources = [headers]
        found = False
        
        for resource in resources[1:]:
            if len(resource) >= 1 and resource[0] == resource_id:
                found = True
                # Update fields if provided
                if title and len(resource) > 1:
                    resource[1] = title
                if category and len(resource) > 2:
                    resource[2] = category
                if content and len(resource) > 3:
                    resource[3] = content
                if tags and len(resource) > 4:
                    resource[4] = tags
            updated_resources.append(resource)
        
        if not found:
            print(f"\n Resource with ID '{resource_id}' not found.\n")
            return False, f"Resource with ID '{resource_id}' not found"
        
        # Write updated resources back to CSV
        Database.update_csv_file(hub.resources_file, updated_resources)
        
        print(f"\n Resource with ID '{resource_id}' updated successfully.\n")
        return True, f"Resource with ID '{resource_id}' updated successfully"
    
    # Educational Hub Methods that forward to User class methods
    def view_educational_resources(self):
        """View all educational resources available in the system."""
        return super().view_educational_resources()
    
    def search_educational_resources(self, query):
        """Search for educational resources by title, category, or tags."""
        return super().search_educational_resources(query)
    
    def view_resource_details(self, resource_id):
        """View detailed information about a specific educational resource."""
        return super().view_resource_details(resource_id)
    
    def get_resources_by_category(self, category):
        """Get all resources in a specific category."""
        return super().get_resources_by_category(category)
    
    def get_latest_resources(self, limit=5):
        """Get the latest educational resources added to the system."""
        return super().get_latest_resources(limit)
    
    # Blockchain Methods
    def view_blockchain_transactions(self):
        """View all transactions in the blockchain."""
        from transactions import TransactionManager
        transaction_manager = TransactionManager()
        return transaction_manager.get_blockchain_transactions()
    
    def verify_blockchain_integrity(self):
        """Verify the integrity of the blockchain."""
        from transactions import TransactionManager
        transaction_manager = TransactionManager()
        is_valid = transaction_manager.verify_blockchain()
        if is_valid:
            print("\n Blockchain integrity verified. All transactions are secure.\n")
        else:
            print("\n Blockchain integrity check failed. There may be tampering.\n")
        return is_valid
    
    def view_smart_contracts(self):
        """View all smart contracts in the system."""
        from transactions import TransactionManager
        transaction_manager = TransactionManager()
        contracts = transaction_manager.blockchain.get_contract_history()
        
        if not contracts:
            print("\n No smart contracts found.\n")
        else:
            print("\n Smart Contract History:")
            for contract in contracts:
                status_symbol = "" if contract["status"] == "Executed" else "⏳"
                print(f"- {status_symbol} Contract ID: {contract['contract_id']} | Status: {contract['status']}")
                print(f"  Buyer: {contract['buyer_id']} | Seller: {contract['seller_id']} | Product: {contract['product_id']}")
                print(f"  Price: ₱{contract['price']:.2f} | Terms: {contract['terms']}")
                if contract["execution_time"]:
                    print(f"  Executed at: {contract['execution_time']}")
                print()
        
        return contracts
    
    def execute_smart_contract(self, contract_id):
        """Execute a smart contract by its ID."""
        from transactions import TransactionManager
        transaction_manager = TransactionManager()
        success, message = transaction_manager.execute_smart_contract(contract_id)
        
        if success:
            print(f"\n Smart contract {contract_id} executed successfully.\n")
        else:
            print(f"\n Failed to execute smart contract: {message}\n")
        
        return success, message
    
    def generate_blockchain_report(self):
        """Generate a comprehensive report on blockchain activity."""
        from transactions import TransactionManager
        transaction_manager = TransactionManager()
        
        # Get blockchain data
        transactions = transaction_manager.blockchain.get_transaction_history()
        contracts = transaction_manager.blockchain.get_contract_history()
        chain_valid = transaction_manager.blockchain.is_chain_valid()
        
        # Calculate statistics
        total_transactions = len(transactions)
        confirmed_transactions = sum(1 for tx in transactions if tx["status"] == "Confirmed")
        pending_transactions = total_transactions - confirmed_transactions
        total_value = sum(tx["amount"] for tx in transactions)
        
        total_contracts = len(contracts)
        executed_contracts = sum(1 for c in contracts if c["status"] == "Executed")
        pending_contracts = total_contracts - executed_contracts
        
        # Display report
        print("\n📊 BLOCKCHAIN ACTIVITY REPORT\n")
        print(f"Blockchain Integrity: {' Valid' if chain_valid else ' Invalid'}")
        print("\nTransaction Statistics:")
        print(f"- Total Transactions: {total_transactions}")
        print(f"- Confirmed: {confirmed_transactions}")
        print(f"- Pending: {pending_transactions}")
        print(f"- Total Value: ₱{total_value:.2f}")
        
        print("\nSmart Contract Statistics:")
        print(f"- Total Contracts: {total_contracts}")
        print(f"- Executed: {executed_contracts}")
        print(f"- Pending: {pending_contracts}")
        
        # Return report data
        report = {
            "blockchain_valid": chain_valid,
            "transactions": {
                "total": total_transactions,
                "confirmed": confirmed_transactions,
                "pending": pending_transactions,
                "value": total_value
            },
            "contracts": {
                "total": total_contracts,
                "executed": executed_contracts,
                "pending": pending_contracts
            }
        }
        
        return True, report
    
    # Blockchain Methods
    def view_blockchain_transactions(self):
        """View all transactions in the blockchain."""
        from transactions import TransactionManager
        transaction_manager = TransactionManager()
        return transaction_manager.get_blockchain_transactions()
    
    def verify_blockchain_integrity(self):
        """Verify the integrity of the blockchain."""
        from transactions import TransactionManager
        transaction_manager = TransactionManager()
        is_valid = transaction_manager.verify_blockchain()
        if is_valid:
            print("\n Blockchain integrity verified. All transactions are secure.\n")
        else:
            print("\n Blockchain integrity check failed. There may be tampering.\n")
        return is_valid
    
    def view_smart_contracts(self):
        """View all smart contracts in the system."""
        from transactions import TransactionManager
        transaction_manager = TransactionManager()
        contracts = transaction_manager.blockchain.get_contract_history()
        
        if not contracts:
            print("\n No smart contracts found.\n")
        else:
            print("\n Smart Contract History:")
            for contract in contracts:
                status_symbol = "" if contract["status"] == "Executed" else "⏳"
                print(f"- {status_symbol} Contract ID: {contract['contract_id']} | Status: {contract['status']}")
                print(f"  Buyer: {contract['buyer_id']} | Seller: {contract['seller_id']} | Product: {contract['product_id']}")
                print(f"  Price: ₱{contract['price']:.2f} | Terms: {contract['terms']}")
                if contract["execution_time"]:
                    print(f"  Executed at: {contract['execution_time']}")
                print()
        
        return contracts
