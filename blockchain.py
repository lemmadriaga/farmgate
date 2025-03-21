import hashlib
import json
import time
import csv
import os
import uuid
from database import Database, DATA_FOLDER

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, nonce=0):
        """Initialize a block in the blockchain"""
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate the hash of the block"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
    
    def mine_block(self, difficulty):
        """Mine a block (Proof of Work)"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"\n✅ Block mined: {self.hash}")
        return self.hash

    def to_dict(self):
        """Convert block to dictionary for serialization"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

class SmartContract:
    def __init__(self, contract_id, buyer_id, seller_id, product_id, price, terms):
        """Initialize a smart contract for a transaction"""
        self.contract_id = contract_id or str(uuid.uuid4())[:8]
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.product_id = product_id
        self.price = price
        self.terms = terms
        self.status = "Created"
        self.creation_time = time.time()
        self.execution_time = None
    
    def execute(self):
        """Execute the smart contract if conditions are met"""
        # Check if all conditions are met
        if self.validate_conditions():
            self.status = "Executed"
            self.execution_time = time.time()
            return True, "Contract executed successfully"
        return False, "Contract conditions not met"
    
    def validate_conditions(self):
        """Validate if all conditions for the contract are met"""
        # In a real system, this would check various conditions
        # For this implementation, we'll assume all conditions are met if the contract exists
        return True
    
    def to_dict(self):
        """Convert smart contract to dictionary for serialization"""
        return {
            "contract_id": self.contract_id,
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
            "product_id": self.product_id,
            "price": self.price,
            "terms": self.terms,
            "status": self.status,
            "creation_time": self.creation_time,
            "execution_time": self.execution_time
        }

class Blockchain:
    def __init__(self):
        """Initialize the blockchain"""
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 2  # Difficulty for mining (number of leading zeros)
        self.mining_reward = 1
        self.smart_contracts = {}
        self.blockchain_file = os.path.join(DATA_FOLDER, "blockchain.csv")
        self.transactions_file = os.path.join(DATA_FOLDER, "blockchain_transactions.csv")
        self.contracts_file = os.path.join(DATA_FOLDER, "smart_contracts.csv")
        
        # Create genesis block if chain is empty
        self.initialize_files()
        if not self.chain:
            self.create_genesis_block()
    
    def initialize_files(self):
        """Initialize blockchain CSV files if they don't exist"""
        # Initialize blockchain file
        if not os.path.isfile(self.blockchain_file):
            with open(self.blockchain_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Index", "Timestamp", "Previous Hash", "Hash", "Nonce", "Transactions"])
        else:
            # Load existing blockchain
            self.load_blockchain()
        
        # Initialize transactions file
        if not os.path.isfile(self.transactions_file):
            with open(self.transactions_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Transaction ID", "Buyer ID", "Seller ID", "Product ID", 
                                "Amount", "Timestamp", "Status", "Block Hash"])
        
        # Initialize smart contracts file
        if not os.path.isfile(self.contracts_file):
            with open(self.contracts_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Contract ID", "Buyer ID", "Seller ID", "Product ID", 
                                "Price", "Terms", "Status", "Creation Time", "Execution Time"])
    
    def load_blockchain(self):
        """Load blockchain from CSV file"""
        try:
            with open(self.blockchain_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 6:
                        # Parse transactions from string to list
                        transactions_str = row[5]
                        try:
                            transactions = json.loads(transactions_str)
                        except:
                            transactions = []
                        
                        # Create block and add to chain
                        block = Block(
                            index=int(row[0]),
                            timestamp=float(row[1]),
                            previous_hash=row[2],
                            transactions=transactions,
                            nonce=int(row[4])
                        )
                        block.hash = row[3]  # Set the hash directly
                        self.chain.append(block)
        except Exception as e:
            print(f"Error loading blockchain: {e}")
            self.chain = []
    
    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_block = Block(0, time.time(), [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        self.save_block_to_csv(genesis_block)
        return genesis_block
    
    def get_latest_block(self):
        """Get the latest block in the blockchain"""
        return self.chain[-1] if self.chain else None
    
    def add_transaction(self, transaction):
        """Add a transaction to pending transactions"""
        self.pending_transactions.append(transaction)
        return True
    
    def mine_pending_transactions(self, miner_address):
        """Mine pending transactions and add them to a new block"""
        if not self.pending_transactions:
            print("\n❌ No transactions to mine")
            return False
        
        # Add mining reward transaction
        self.pending_transactions.append({
            "sender": "System",
            "recipient": miner_address,
            "amount": self.mining_reward,
            "type": "reward"
        })
        
        # Create new block
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1 if latest_block else 0,
            timestamp=time.time(),
            transactions=self.pending_transactions,
            previous_hash=latest_block.hash if latest_block else "0"
        )
        
        # Mine the block
        new_block.mine_block(self.difficulty)
        
        # Add block to chain
        self.chain.append(new_block)
        
        # Save block to CSV
        self.save_block_to_csv(new_block)
        
        # Update transaction statuses
        self.update_transaction_statuses(new_block)
        
        # Clear pending transactions
        self.pending_transactions = []
        
        return True
    
    def save_block_to_csv(self, block):
        """Save a block to the blockchain CSV file"""
        with open(self.blockchain_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                block.index,
                block.timestamp,
                block.previous_hash,
                block.hash,
                block.nonce,
                json.dumps(block.transactions)
            ])
    
    def update_transaction_statuses(self, block):
        """Update transaction statuses in the transactions CSV file"""
        for transaction in block.transactions:
            if transaction.get("type") != "reward":  # Skip reward transactions
                # Add transaction to blockchain_transactions.csv
                with open(self.transactions_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        transaction.get("id", str(uuid.uuid4())[:8]),
                        transaction.get("buyer_id", ""),
                        transaction.get("seller_id", ""),
                        transaction.get("product_id", ""),
                        transaction.get("amount", 0),
                        transaction.get("timestamp", time.time()),
                        "Confirmed",
                        block.hash
                    ])
    
    def is_chain_valid(self):
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if hash is correct
            if current_block.hash != current_block.calculate_hash():
                print(f"\n❌ Invalid hash for block {i}: {current_block.hash}")
                return False
            
            # Check if previous hash reference is correct
            if current_block.previous_hash != previous_block.hash:
                print(f"\n❌ Invalid previous hash reference for block {i}")
                return False
        
        print("\n✅ Blockchain is valid")
        return True
    
    def create_smart_contract(self, buyer_id, seller_id, product_id, price, terms):
        """Create a new smart contract for a transaction"""
        contract_id = str(uuid.uuid4())[:8]
        contract = SmartContract(contract_id, buyer_id, seller_id, product_id, price, terms)
        self.smart_contracts[contract_id] = contract
        
        # Save contract to CSV
        with open(self.contracts_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                contract.contract_id,
                contract.buyer_id,
                contract.seller_id,
                contract.product_id,
                contract.price,
                contract.terms,
                contract.status,
                contract.creation_time,
                contract.execution_time or ""
            ])
        
        return contract_id
    
    def execute_smart_contract(self, contract_id):
        """Execute a smart contract by its ID"""
        if contract_id not in self.smart_contracts:
            # Try to load from CSV
            contract = self.load_contract_from_csv(contract_id)
            if not contract:
                return False, f"Contract {contract_id} not found"
            self.smart_contracts[contract_id] = contract
        
        contract = self.smart_contracts[contract_id]
        success, message = contract.execute()
        
        if success:
            # Update contract in CSV
            self.update_contract_in_csv(contract)
            
            # Create transaction from contract
            transaction = {
                "id": str(uuid.uuid4())[:8],
                "buyer_id": contract.buyer_id,
                "seller_id": contract.seller_id,
                "product_id": contract.product_id,
                "amount": contract.price,
                "timestamp": time.time(),
                "contract_id": contract_id,
                "type": "contract_execution"
            }
            
            # Add transaction to pending
            self.add_transaction(transaction)
            
            # Also update the transaction status in transactions.csv
            self._update_transaction_in_csv(contract)
        
        return success, message
        
    def _update_transaction_in_csv(self, contract):
        """Update the transaction status in transactions.csv to Approved"""
        import csv
        import os
        
        transaction_file = os.path.join(DATA_FOLDER, "transactions.csv")
        updated_transactions = []
        transaction_found = False
        
        try:
            # Read all transactions
            with open(transaction_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                headers = next(reader)  # Get header row
                updated_transactions.append(headers)
                
                # Get blockchain transactions to find the transaction ID related to this contract
                blockchain_transactions = self.get_transaction_history()
                related_transaction_ids = []
                
                # Find transaction IDs related to this contract's product_id
                for tx in blockchain_transactions:
                    if tx['product_id'] == contract.product_id and tx['buyer_id'] == contract.buyer_id:
                        related_transaction_ids.append(tx['id'])
                
                # Now process the transactions.csv file
                for row in reader:
                    # Check if this transaction matches any of the related transaction IDs
                    if len(row) >= 5 and row[3] == "Pending":
                        # In transactions.csv: [Buyer Name, Product Name, Price, Status, Transaction ID]
                        if row[4] in related_transaction_ids:
                            row[3] = "Approved"  # Update status to Approved
                            transaction_found = True
                            print(f"\n✅ Transaction {row[4]} for {row[1]} approved in traditional system.\n")
                    updated_transactions.append(row)
            
            # Write back all transactions if any were updated
            if transaction_found:
                with open(transaction_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(updated_transactions)
            else:
                # If no exact match found, try to match by product name
                with open(transaction_file, mode='r', newline='') as file:
                    reader = csv.reader(file)
                    headers = next(reader)  # Get header row
                    updated_transactions = [headers]
                    
                    for row in reader:
                        if len(row) >= 5 and row[3] == "Pending" and row[1] == contract.product_id:
                            row[3] = "Approved"  # Update status to Approved
                            transaction_found = True
                            print(f"\n✅ Transaction for {row[1]} approved in traditional system.\n")
                        updated_transactions.append(row)
                
                if transaction_found:
                    with open(transaction_file, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(updated_transactions)
        except Exception as e:
            print(f"Error updating transaction in CSV: {e}")
    
    def load_contract_from_csv(self, contract_id):
        """Load a specific contract from CSV by ID"""
        try:
            with open(self.contracts_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 9 and row[0] == contract_id:
                        contract = SmartContract(
                            contract_id=row[0],
                            buyer_id=row[1],
                            seller_id=row[2],
                            product_id=row[3],
                            price=float(row[4]),
                            terms=row[5]
                        )
                        contract.status = row[6]
                        contract.creation_time = float(row[7])
                        contract.execution_time = float(row[8]) if row[8] else None
                        return contract
        except Exception as e:
            print(f"Error loading contract: {e}")
        return None
    
    def update_contract_in_csv(self, contract):
        """Update a contract in the CSV file"""
        contracts = []
        try:
            # Read all contracts
            with open(self.contracts_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                headers = next(reader)
                contracts.append(headers)
                for row in reader:
                    if len(row) >= 9 and row[0] == contract.contract_id:
                        # Update contract
                        contracts.append([
                            contract.contract_id,
                            contract.buyer_id,
                            contract.seller_id,
                            contract.product_id,
                            contract.price,
                            contract.terms,
                            contract.status,
                            contract.creation_time,
                            contract.execution_time or ""
                        ])
                    else:
                        contracts.append(row)
            
            # Write back all contracts
            with open(self.contracts_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(contracts)
        except Exception as e:
            print(f"Error updating contract: {e}")
    
    def validate_transaction(self, transaction):
        """Validate a transaction before adding it to the blockchain"""
        # Check if transaction has required fields
        required_fields = ["buyer_id", "seller_id", "product_id", "amount"]
        for field in required_fields:
            if field not in transaction:
                return False, f"Missing required field: {field}"
        
        # In a real system, we would check signatures, balances, etc.
        # For this implementation, we'll just validate the structure
        
        return True, "Transaction is valid"
    
    def store_transaction(self, transaction):
        """Store a validated transaction in the blockchain"""
        # First validate the transaction
        is_valid, message = self.validate_transaction(transaction)
        if not is_valid:
            return False, message
        
        # Add transaction to pending transactions
        transaction["timestamp"] = time.time()
        transaction["id"] = transaction.get("id", str(uuid.uuid4())[:8])
        self.add_transaction(transaction)
        
        # Also store in transactions file with status "Pending"
        with open(self.transactions_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                transaction["id"],
                transaction["buyer_id"],
                transaction["seller_id"],
                transaction["product_id"],
                transaction["amount"],
                transaction["timestamp"],
                "Pending",
                ""  # Block hash will be filled when mined
            ])
        
        return True, "Transaction added to pending transactions"
    
    def get_transaction_history(self, user_id=None):
        """Get transaction history, optionally filtered by user ID"""
        transactions = []
        try:
            with open(self.transactions_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                headers = next(reader)
                for row in reader:
                    if len(row) >= 8:
                        # Filter by user ID if provided
                        if user_id and row[1] != user_id and row[2] != user_id:
                            continue
                        
                        transactions.append({
                            "id": row[0],
                            "buyer_id": row[1],
                            "seller_id": row[2],
                            "product_id": row[3],
                            "amount": float(row[4]),
                            "timestamp": float(row[5]),
                            "status": row[6],
                            "block_hash": row[7]
                        })
        except Exception as e:
            print(f"Error getting transaction history: {e}")
        
        return transactions
        
    def store_product_listing(self, product_id, farmer_id, product_name, price):
        """Store a product listing in the blockchain"""
        # Create a product listing transaction
        listing_transaction = {
            "id": str(uuid.uuid4())[:8],
            "type": "product_listing",
            "farmer_id": farmer_id,
            "product_id": product_id,
            "product_name": product_name,
            "price": float(price) if isinstance(price, str) else price,
            "timestamp": time.time(),
            "status": "Active"
        }
        
        # Add transaction to pending transactions
        self.add_transaction(listing_transaction)
        
        # Mine pending transactions to add to blockchain
        # Using farmer_id as the miner address for reward
        self.mine_pending_transactions(farmer_id)
        
        return True, "Product listing stored in blockchain"
    
    def get_contract_history(self, user_id=None):
        """Get contract history, optionally filtered by user ID"""
        contracts = []
        try:
            with open(self.contracts_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                headers = next(reader)
                for row in reader:
                    if len(row) >= 9:
                        # Filter by user ID if provided
                        if user_id and row[1] != user_id and row[2] != user_id:
                            continue
                        
                        contracts.append({
                            "contract_id": row[0],
                            "buyer_id": row[1],
                            "seller_id": row[2],
                            "product_id": row[3],
                            "price": float(row[4]),
                            "terms": row[5],
                            "status": row[6],
                            "creation_time": float(row[7]),
                            "execution_time": float(row[8]) if row[8] else None
                        })
        except Exception as e:
            print(f"Error getting contract history: {e}")
        
        return contracts
