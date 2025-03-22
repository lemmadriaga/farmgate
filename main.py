from user import User
from farmer import Farmer
from buyer import Buyer
from marketplace import Marketplace
from admin import Admin
from transactions import TransactionManager
from loan_system import LoanSystem
from educational_hub import EducationalHub
import time

def main():
    user = User()  # Create a base User instance for registration/login

    print("\n Welcome to FarmGate Console System \n")

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role (farmer/buyer/admin): ").lower()
            email = input("Enter email: ")

            success, message = user.register(username, password, role, email)
            print("\n✅ " + message if success else "\n " + message)

            if success:
                print("\n🔄 Logging you in automatically...\n")
                # The user object is already populated with user details after registration
                user_details = user.get_user_details()

                if user_details:
                    print(f"\n✅ Proceeding to system with user_id: {user_details['user_id']}")
                    start_system(user_details["user_id"], username, user_details["role"])
                    break  
                else:
                    print("\n ERROR: User details not found. Please log in manually.")

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")

            success, result = user.login(username, password)
            
            if success:
                user_details = result  # result contains user details on successful login
                print(f"\n✅ Login successful! Welcome, {username} (User ID: {user_details['user_id']})")
                start_system(user_details["user_id"], username, user_details["role"])
                break  
            else:
                print(f"\n {result}")  # result contains error message on failed login

        elif choice == "3":
            print("\n Exiting FarmGate System. Thank you! \n")
            break

        else:
            print("\n Invalid choice. Please enter a number from 1-3.\n")
1

def start_system(user_id, username, role):
    transaction_manager = TransactionManager()

    # Create the appropriate user object based on role
    if role == "farmer":
        user = Farmer(username, "N/A", user_id=user_id)
    elif role == "buyer":
        user = Buyer(username, "N/A", user_id=user_id)
    elif role == "admin":
        user = Admin(username, user_id=user_id)
    else:
        print("\n Invalid role. Logging out.\n")
        return

    # Display role-specific menu
    while True:
        print("\n===== FarmGate System Menu =====\n")
        
        # Common options for all users
        print("Common Options:")
        print("1. View Marketplace")
        print("2. View Transactions")
        print("3. Educational Hub")
        
        # Role-specific options
        if role == "farmer":
            print("\nFarmer Options:")
            print("4. List Produce")
            print("5. Apply for Loan")
            print("6. View My Loans")
            print("7. Make Loan Repayment")
        elif role == "buyer":
            print("\nBuyer Options:")
            print("4. Purchase Produce")
        elif role == "admin":
            print("\nAdmin Options:")
            print("4. Approve Transaction")
            print("5. View Pending Loans")
            print("6. Approve/Reject Loan")
            print("7. Manage Users")
            print("8. Generate Reports")
            print("9. Manage Educational Resources")
            print("\nBlockchain Options:")
            print("10. View Blockchain Transactions")
            print("11. Verify Blockchain Integrity")
            print("12. View Smart Contracts")
            print("13. Execute Smart Contract")
            print("14. Generate Blockchain Report")
        
        print("\n0. Logout")
        choice = input("\nEnter your choice: ")

        # Common options
        if choice == "1":  # View Marketplace
            Marketplace.display_products()
            
        elif choice == "2":  # View Transactions
            transaction_manager.get_transactions()
            
        elif choice == "3":  # Educational Hub
            print("\n===== Educational Hub =====\n")
            print("1. View All Resources")
            print("2. Search Resources")
            print("3. View Latest Resources")
            print("4. View Resources by Category")
            print("5. View Resource Details")
            print("0. Back to Main Menu")
            
            edu_choice = input("\nEnter your choice: ")
            
            if edu_choice == "1":
                user.view_educational_resources()
            elif edu_choice == "2":
                query = input("Enter search term: ")
                user.search_educational_resources(query)
            elif edu_choice == "3":
                limit = int(input("How many resources to view? (default: 5): ") or "5")
                user.get_latest_resources(limit)
            elif edu_choice == "4":
                print("\nCategories: Farming, Market, Finance, Certification")
                category = input("Enter category: ")
                user.get_resources_by_category(category)
            elif edu_choice == "5":
                resource_id = input("Enter Resource ID: ")
                user.view_resource_details(resource_id)
            elif edu_choice == "0":
                pass
            else:
                print("\n Invalid choice.\n")

        # Farmer options
        elif choice == "4" and role == "farmer":  # List Produce
            product_name = input("Enter produce name: ")
            price = float(input("Enter price (₱): "))
            user.list_produce(product_name, price)
            
        elif choice == "5" and role == "farmer":  # Apply for Loan
            loan_amount = float(input("Enter loan amount (₱): "))
            interest_rate = float(input("Enter interest rate (%): "))
            user.apply_for_loan(loan_amount, interest_rate)
            
        elif choice == "6" and role == "farmer":  # View My Loans
            user.view_my_loans()
            
        elif choice == "7" and role == "farmer":  # Make Loan Repayment
            # First show the farmer's loans
            loans = user.view_my_loans()
            if loans:
                loan_id = input("Enter Loan ID to make a repayment: ")
                amount = float(input("Enter repayment amount (₱): "))
                user.make_loan_repayment(loan_id, amount)

        # Buyer options
        elif choice == "4" and role == "buyer":  # Purchase Produce
            Marketplace.display_products()
            product_id = input("Enter Product ID to purchase: ")
            user.purchase_produce(product_id)

        # Admin options
        elif choice == "3" and role == "admin":  # Approve Transaction
            print("\n1. Approve by Buyer/Product Name")
            print("2. Approve by Transaction ID")
            approve_choice = input("Enter choice: ")
            
            if approve_choice == "1":
                buyer_name = input("Enter Buyer Name: ")
                product_name = input("Enter Product Name: ")
                user.approve_transaction(buyer_name=buyer_name, product_name=product_name)
            elif approve_choice == "2":
                transaction_id = input("Enter Transaction ID: ")
                user.approve_transaction(transaction_id=transaction_id)
            else:
                print("\n Invalid choice.\n")
            
        elif choice == "4" and role == "admin":  # View Pending Loans
            user.view_all_loans(status="Pending")
            
        elif choice == "5" and role == "admin":  # Approve/Reject Loan
            loan_id = input("Enter Loan ID: ")
            approval = input("Approve this loan? (yes/no): ").lower()
            approved = approval == "yes"
            user.approve_loan(loan_id, approved)
            
        elif choice == "6" and role == "admin":  # Manage Users
            print("\n1. View All Users\n2. Delete User")
            admin_choice = input("Enter choice: ")
            
            if admin_choice == "1":
                user.manage_users("view")
            elif admin_choice == "2":
                user_id_to_delete = input("Enter User ID to delete: ")
                success, message = user.manage_users("delete", user_id=user_id_to_delete)
                print("\n✅ " + message if success else "\n " + message)
                
        elif choice == "7" and role == "admin":  # Generate Reports
            print("\n1. Transaction Report\n2. User Report\n3. Loan Report\n4. Educational Resources Report\n5. Blockchain Report")
            report_choice = input("Enter choice: ")
            
            if report_choice == "1":
                user.generate_report("transactions")
            elif report_choice == "2":
                user.generate_report("users")
            elif report_choice == "3":
                user.generate_report("loans")
            elif report_choice == "4":
                user.generate_report("education")
            elif report_choice == "5":
                user.generate_blockchain_report()
            else:
                print("\n Invalid report type!")
                
        elif choice == "9" and role == "admin":  # Manage Educational Resources
            print("\n===== Manage Educational Resources =====\n")
            print("1. View All Resources")
            print("2. Add New Resource")
            print("3. Update Resource")
            print("4. Delete Resource")
            print("0. Back to Main Menu")
            
            edu_admin_choice = input("\nEnter your choice: ")
            
            if edu_admin_choice == "1":
                hub = EducationalHub()
                hub.view_all_resources()
            elif edu_admin_choice == "2":
                title = input("Enter resource title: ")
                print("\nCategories: Farming, Market, Finance, Certification")
                category = input("Enter category: ")
                content = input("Enter resource content: ")
                tags = input("Enter tags (comma-separated): ")
                user.add_educational_resource(title, category, content, tags)
            elif edu_admin_choice == "3":
                # First show all resources
                hub = EducationalHub()
                hub.view_all_resources()
                
                resource_id = input("\nEnter Resource ID to update: ")
                title = input("Enter new title (leave empty to keep current): ")
                category = input("Enter new category (leave empty to keep current): ")
                content = input("Enter new content (leave empty to keep current): ")
                tags = input("Enter new tags (leave empty to keep current): ")
                
                user.update_educational_resource(
                    resource_id,
                    title=title if title else None,
                    category=category if category else None,
                    content=content if content else None,
                    tags=tags if tags else None
                )
            elif edu_admin_choice == "4":
                # First show all resources
                hub = EducationalHub()
                hub.view_all_resources()
                
                resource_id = input("\nEnter Resource ID to delete: ")
                user.delete_educational_resource(resource_id)
            elif edu_admin_choice == "0":
                pass
            else:
                print("\n Invalid choice.\n")
                
        elif choice == "8" and role == "admin":  # Generate Reports
            print("\n1. Transaction Report\n2. User Report\n3. Loan Report\n4. Educational Resources Report")
            report_choice = input("Enter choice: ")
            
            if report_choice == "1":
                user.generate_report("transactions")
            elif report_choice == "2":
                user.generate_report("users")
            elif report_choice == "3":
                user.generate_report("loans")
            elif report_choice == "4":
                user.generate_report("education")
            else:
                print("\n Invalid report type!")

        # Blockchain options for admin
        elif choice == "10" and role == "admin":  # View Blockchain Transactions
            user.view_blockchain_transactions()
            
        elif choice == "11" and role == "admin":  # Verify Blockchain Integrity
            user.verify_blockchain_integrity()
            
        elif choice == "12" and role == "admin":  # View Smart Contracts
            user.view_smart_contracts()
            
        elif choice == "13" and role == "admin":  # Execute Smart Contract
            contract_id = input("Enter Smart Contract ID to execute: ")
            user.execute_smart_contract(contract_id)
            
        elif choice == "14" and role == "admin":  # Generate Blockchain Report
            user.generate_blockchain_report()
            
        elif choice == "0":
            print("\n Logging out...\n")
            break

        else:
            print("\n Invalid choice or insufficient privileges.\n")

        time.sleep(1)

if __name__ == "__main__":
    main()
