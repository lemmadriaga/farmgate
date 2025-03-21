from login import Login
from signup import Signup
from farmer import Farmer
from buyer import Buyer
from marketplace import Marketplace
from admin import Admin
from transactions import TransactionManager
import time

def main():
    login = Login()
    signup = Signup()

    print("\n Welcome to FarmGate Console System \n")

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role (farmer/buyer/admin): ").lower()
            email = input("Enter email: ")

            success, message = signup.register_user(username, password, role, email)
            print("\n✅ " + message if success else "\n❌ " + message)

            if success:
                print("\n🔄 Logging you in automatically...\n")
                user_details = login.get_user_details(username)

                if user_details:
                    print(f"\n✅ DEBUG: Proceeding to system with user_id: {user_details['user_id']}")
                    start_system(user_details["user_id"], username, user_details["role"])
                    break  
                else:
                    print("\n❌ ERROR: User details not found. Please log in manually.")

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")

            if login.authenticate_user(username, password):
                user_details = login.get_user_details(username)
                print(f"\n✅ Login successful! Welcome, {username} (User ID: {user_details['user_id']})")
                start_system(user_details["user_id"], username, user_details["role"])
                break  
            else:
                print("\n❌ Invalid username or password!")

        elif choice == "3":
            print("\n Exiting FarmGate System. Thank you! \n")
            break

        else:
            print("\n Invalid choice. Please enter a number from 1-3.\n")
1

def start_system(user_id, username, role):
    transaction_manager = TransactionManager()

    while True:
        print("\n1. Farmer List Produce\n2. Buyer Purchase Produce\n3. View Marketplace\n4. View Transactions\n5. Admin Approve Transaction\n6. Logout")
        choice = input("\nEnter your choice: ")

        if choice == "1" and role == "farmer":
            product_name = input("Enter produce name: ")
            price = float(input("Enter price (₱): "))
            farmer = Farmer(username, "N/A")
            farmer.list_produce(product_name, price)

        elif choice == "2" and role == "buyer":
            Marketplace.display_products()
            product_name = input("Enter Product Name to purchase: ")
            price = float(input("Enter Price: ₱"))
            buyer = Buyer(username, "N/A")
            transaction_manager.record_transaction(buyer.name, product_name, price)

        elif choice == "3":
            Marketplace.display_products()

        elif choice == "4":
            transaction_manager.get_transactions()

        elif choice == "5" and role == "admin":
            buyer_name = input("Enter Buyer Name: ")
            product_name = input("Enter Product Name: ")
            admin = Admin(username)
            admin.approve_transaction(buyer_name, product_name)

        elif choice == "6":
            print("\n Logging out...\n")
            break

        else:
            print("\n Invalid choice or insufficient privileges.\n")

        time.sleep(1)

if __name__ == "__main__":
    main()
