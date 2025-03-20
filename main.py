from farmer import Farmer
from buyer import Buyer
from marketplace import Marketplace
from admin import Admin
from transactions import TransactionManager
import time

def main():
    print("\n Welcome to FarmGate Console System \n")

    # Create instances
    farmer1 = Farmer("Kuya Obet", "0923-456-7890")
    buyer1 = Buyer("Juan Dela Cruz", "0917-123-4567")
    admin1 = Admin("Ms. Admin")
    transaction_manager = TransactionManager()

    while True:
        print("\n1. Farmer List Produce\n2. Buyer Purchase Produce\n3. View Marketplace\n4. View Transactions\n5. Admin Approve Transaction\n6. Exit")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            product_name = input("Enter produce name: ")
            price = float(input("Enter price (₱): "))
            farmer1.list_produce(product_name, price)

        elif choice == "2":
            Marketplace.display_products()
            product_name = input("Enter Product Name to purchase: ")
            price = float(input("Enter Price: ₱"))
            transaction_manager.record_transaction(buyer1.name, product_name, price)

        elif choice == "3":
            Marketplace.display_products()

        elif choice == "4":
            transaction_manager.get_transactions()

        elif choice == "5":
            buyer_name = input("Enter Buyer Name: ")
            product_name = input("Enter Product Name: ")
            transaction_manager.approve_transaction(buyer_name, product_name)

        elif choice == "6":
            print("\n Exiting FarmGate System. Thank you! \n")
            break

        else:
            print("\n Invalid choice. Please enter a number from 1-6.\n")

        time.sleep(1)

if __name__ == "__main__":
    main()
