import csv
import os

# Ensure data folder exists
DATA_FOLDER = "data"
TRANSACTION_FILE = os.path.join(DATA_FOLDER, "transactions.csv")

# Transaction Manager
class TransactionManager:
    def __init__(self):
        # Ensure the file exists with headers
        if not os.path.isfile(TRANSACTION_FILE):
            with open(TRANSACTION_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Buyer Name", "Product Name", "Price", "Status"])

    def record_transaction(self, buyer_name, product_name, price, status="Pending"):
        """Stores transaction data into CSV file."""
        with open(TRANSACTION_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([buyer_name, product_name, price, status])
        print(f"\n Transaction recorded: {buyer_name} purchased {product_name} for ₱{price:.2f} ({status})\n")

    def get_transactions(self):
        """Retrieves all transactions from the CSV file."""
        if not os.path.isfile(TRANSACTION_FILE):
            print("\n No transactions found.\n")
            return []
        
        with open(TRANSACTION_FILE, mode='r') as file:
            reader = csv.reader(file)
            transactions = list(reader)[1:]  
        
        if not transactions:
            print("\n  No transactions recorded yet.\n")
        else:
            print("\n Transaction History:")
            for t in transactions:
                try:
                    # Check if transaction has enough elements
                    if len(t) >= 4:
                        print(f"- Buyer: {t[1]} | Product: {t[2]} | Price: ₱{t[3]} | Status: {t[4]}")
                    else:
                        print(f"- Nothing else yet...: {', '.join(t)}")
                except Exception as e:
                    print(f"- Error displaying transaction: {e}")
        print()
        return transactions

    def approve_transaction(self, buyer_name, product_name):
        """Updates transaction status to Approved."""
        transactions = self.get_transactions()
        updated_transactions = []
        found = False

        for transaction in transactions:
            if transaction[0] == buyer_name and transaction[1] == product_name and transaction[3] == "Pending":
                transaction[3] = "Approved"
                found = True
            updated_transactions.append(transaction)

        if found:
            with open(TRANSACTION_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Buyer Name", "Product Name", "Price", "Status"])
                writer.writerows(updated_transactions)
            print(f"\n Transaction Approved for {buyer_name}: {product_name}\n")
        else:
            print("\n Transaction not found or already approved.\n")
