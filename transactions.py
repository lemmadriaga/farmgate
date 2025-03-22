import csv
import os
import uuid
import time
from blockchain import Blockchain

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
                writer.writerow(["Buyer Name", "Product Name", "Price", "Status", "Transaction ID"])
        
        # Initialize blockchain
        self.blockchain = Blockchain()

    def record_transaction(self, buyer_id, buyer_name, seller_id, product_id, product_name, price, status="Pending"):
        """Stores transaction data into CSV file and blockchain."""
        # Generate transaction ID
        transaction_id = str(uuid.uuid4())[:8]
        
        # Record in traditional CSV for backward compatibility
        with open(TRANSACTION_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # File is empty, write header
                writer.writerow(["Buyer Name", "Product Name", "Price", "Status", "Transaction ID"])
            writer.writerow([buyer_name, product_name, price, status, transaction_id])
        
        # Create blockchain transaction
        transaction = {
            "id": transaction_id,
            "buyer_id": buyer_id,
            "seller_id": seller_id,
            "product_id": product_id,
            "amount": float(price) if isinstance(price, str) else price,
            "timestamp": time.time(),
            "product_name": product_name
        }
        
        # Validate and store transaction in blockchain
        is_valid, message = self.blockchain.validate_transaction(transaction)
        if is_valid:
            success, _ = self.blockchain.store_transaction(transaction)
            if success:
                price_float = float(price) if isinstance(price, str) else price
                print(f"\n✅ Transaction recorded securely: {buyer_name} purchased {product_name} for ₱{price_float:.2f} ({status})")
                print(f"   Transaction ID: {transaction_id} (secured by blockchain)\n")
                return transaction_id
            else:
                price_float = float(price) if isinstance(price, str) else price
                print(f"\n⚠️ Transaction recorded in traditional system only: {buyer_name} purchased {product_name} for ₱{price_float:.2f} ({status})\n")
        else:
            print(f"\n⚠️ Invalid transaction: {message}\n")
        
        return transaction_id

    def get_transactions(self, show_output=True):
        """Retrieves all transactions from the CSV file."""
        if not os.path.isfile(TRANSACTION_FILE):
            if show_output:
                print("\n No transactions found.\n")
            return []
        
        with open(TRANSACTION_FILE, mode='r') as file:
            reader = csv.reader(file)
            transactions = list(reader)[1:]  
        
        if show_output:
            if not transactions:
                print("\n  No transactions recorded yet.\n")
            else:
                print("\n Transaction History:")
                for t in transactions:
                    try:
                        # Check if transaction has enough elements
                        if len(t) >= 4:
                            status_symbol = "✅" if t[3] == "Approved" else "⏳"
                            tx_id = f" | ID: {t[4]}" if len(t) >= 5 else ""
                            print(f"- {status_symbol} Buyer: {t[0]} | Product: {t[1]} | Price: ₱{t[2]} | Status: {t[3]}{tx_id}")
                        else:
                            print(f"- Nothing else yet...: {', '.join(t)}")
                    except Exception as e:
                        print(f"- Error displaying transaction: {e}")
                print()
        return transactions
        
    def get_blockchain_transactions(self, user_id=None):
        """Get transactions from the blockchain."""
        transactions = self.blockchain.get_transaction_history(user_id)
        
        if not transactions:
            print("\n No blockchain transactions found.\n")
        else:
            print("\n Blockchain Transaction History:")
            for tx in transactions:
                status_symbol = "✅" if tx["status"] == "Confirmed" else "⏳"
                print(f"- {status_symbol} ID: {tx['id']} | Amount: ₱{tx['amount']:.2f} | Status: {tx['status']}")
                print(f"  Buyer: {tx['buyer_id']} | Seller: {tx['seller_id']} | Product: {tx['product_id']}")
                if tx["block_hash"]:
                    print(f"  Secured in block: {tx['block_hash'][:10]}...")
                print()
        
        return transactions
    
    def create_smart_contract(self, buyer_id, seller_id, product_id, price, terms="Standard purchase agreement"):
        """Create a smart contract for a transaction."""
        contract_id = self.blockchain.create_smart_contract(buyer_id, seller_id, product_id, price, terms)
        print(f"\n✅ Smart contract created for purchase")
        print(f"   Contract ID: {contract_id}\n")
        return contract_id
    
    def execute_smart_contract(self, contract_id):
        """Execute a smart contract by its ID."""
        success, message = self.blockchain.execute_smart_contract(contract_id)
        if success:
            print(f"\n✅ Smart contract executed successfully: {contract_id}\n")
            # Mine the blockchain to confirm the transaction
            self.blockchain.mine_pending_transactions("admin")
        else:
            print(f"\n Failed to execute smart contract: {message}\n")
        return success, message
    
    def verify_blockchain(self):
        """Verify the integrity of the blockchain."""
        return self.blockchain.is_chain_valid()

    def approve_transaction(self, transaction_id):
        """Updates transaction status to Approved and mines the blockchain."""
        transactions = self.get_transactions()
        updated_transactions = []
        found = False
        buyer_name = ""
        product_name = ""

        # Update in traditional system
        for transaction in transactions:
            if len(transaction) >= 5 and transaction[4] == transaction_id and transaction[3] == "Pending":
                transaction[3] = "Approved"
                found = True
                buyer_name = transaction[0]
                product_name = transaction[1]
            updated_transactions.append(transaction)

        if found:
            # Update CSV file
            with open(TRANSACTION_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Buyer Name", "Product Name", "Price", "Status", "Transaction ID"])
                writer.writerows(updated_transactions)
            
            # Mine pending transactions in blockchain
            self.blockchain.mine_pending_transactions("admin")
            
            print(f"\n✅ Transaction Approved for {buyer_name}: {product_name}")
            print(f"   Transaction ID: {transaction_id} (secured by blockchain)\n")
            return True, f"Transaction {transaction_id} approved successfully"
        else:
            print("\n Transaction not found or already approved.\n")
            return False, "Transaction not found or already approved"
