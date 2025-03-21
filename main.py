from user import User
from farmer import Farmer
from buyer import Buyer
from marketplace import Marketplace
from admin import Admin
from transactions import TransactionManager
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
            print("\n✅ " + message if success else "\n❌ " + message)

            if success:
                print("\n🔄 Logging you in automatically...\n")
                # The user object is already populated with user details after registration
                user_details = user.get_user_details()

                if user_details:
                    print(f"\n✅ Proceeding to system with user_id: {user_details['user_id']}")
                    start_system(user_details["user_id"], username, user_details["role"])
                    break  
                else:
                    print("\n❌ ERROR: User details not found. Please log in manually.")

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
                print(f"\n❌ {result}")  # result contains error message on failed login

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
        print("\n❌ Invalid role. Logging out.\n")
        return

    # Display role-specific menu
    while True:
        print("\n===== FarmGate System Menu =====\n")
        
        # Common options for all users
        print("Common Options:")
        print("1. View Marketplace")
        print("2. View Transactions")
        
        # Role-specific options
        if role == "farmer":
            print("\nFarmer Options:")
            print("3. List Produce")
            print("4. Apply for Loan")
        elif role == "buyer":
            print("\nBuyer Options:")
            print("3. Purchase Produce")
        elif role == "admin":
            print("\nAdmin Options:")
            print("3. Approve Transaction")
            print("4. Approve Loan")
            print("5. Manage Users")
            print("6. Generate Reports")
        
        print("\n0. Logout")
        choice = input("\nEnter your choice: ")

        # Common options
        if choice == "1":  # View Marketplace
            Marketplace.display_products()
            
        elif choice == "2":  # View Transactions
            transaction_manager.get_transactions()

        # Farmer options
        elif choice == "3" and role == "farmer":  # List Produce
            product_name = input("Enter produce name: ")
            price = float(input("Enter price (₱): "))
            user.list_produce(product_name, price)
            
        elif choice == "4" and role == "farmer":  # Apply for Loan
            loan_amount = float(input("Enter loan amount (₱): "))
            interest_rate = float(input("Enter interest rate (%): "))
            user.apply_for_loan(loan_amount, interest_rate)

        # Buyer options
        elif choice == "3" and role == "buyer":  # Purchase Produce
            Marketplace.display_products()
            product_id = input("Enter Product ID to purchase: ")
            user.purchase_produce(product_id)

        # Admin options
        elif choice == "3" and role == "admin":  # Approve Transaction
            buyer_name = input("Enter Buyer Name: ")
            product_name = input("Enter Product Name: ")
            user.approve_transaction(buyer_name, product_name)
            
        elif choice == "4" and role == "admin":  # Approve Loan
            farmer_id = input("Enter Farmer ID: ")
            loan_amount = float(input("Enter Loan Amount: "))
            user.approve_loan(farmer_id, loan_amount)
            
        elif choice == "5" and role == "admin":  # Manage Users
            print("\n1. View All Users\n2. Delete User")
            admin_choice = input("Enter choice: ")
            
            if admin_choice == "1":
                user.manage_users("view")
            elif admin_choice == "2":
                user_id_to_delete = input("Enter User ID to delete: ")
                success, message = user.manage_users("delete", user_id=user_id_to_delete)
                print("\n✅ " + message if success else "\n❌ " + message)
                
        elif choice == "6" and role == "admin":  # Generate Reports
            print("\n1. Transaction Report\n2. User Report\n3. Loan Report")
            report_choice = input("Enter choice: ")
            
            if report_choice == "1":
                user.generate_report("transactions")
            elif report_choice == "2":
                user.generate_report("users")
            elif report_choice == "3":
                user.generate_report("loans")
            else:
                print("\n❌ Invalid report type!")

        elif choice == "6":
            print("\n Logging out...\n")
            break

        else:
            print("\n Invalid choice or insufficient privileges.\n")

        time.sleep(1)

if __name__ == "__main__":
    main()
