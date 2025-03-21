from database import Database
import uuid
from user import User

class Buyer(User):
    def __init__(self, name, contact_info=None, user_id=None, email=None, password=None):
        # Call the parent class constructor
        super().__init__(user_id=user_id, name=name, email=email, password=password, role="buyer")
        self.contact_info = contact_info
        self.purchase_history = []

    def purchase_produce(self, product_id):
        from transactions import TransactionManager
        
        products = Database.read_from_csv("marketplace.csv")
        for product in products:
            if product[0] == product_id:
                seller_id = product[0]
                seller_name = product[1]
                product_name = product[2]
                price = product[3]
                
                # Create transaction manager
                transaction_manager = TransactionManager()
                
                # Record transaction with blockchain integration
                transaction_id = transaction_manager.record_transaction(
                    buyer_id=self.user_id,
                    buyer_name=self.name,
                    seller_id=seller_id,
                    product_id=product_id,
                    product_name=product_name,
                    price=price,
                    status="Pending"
                )
                
                # Create smart contract for the purchase
                contract_id = transaction_manager.create_smart_contract(
                    buyer_id=self.user_id,
                    seller_id=seller_id,
                    product_id=product_id,
                    price=float(price)
                )
                
                # Add to purchase history
                self.purchase_history.append({
                    "product_name": product_name,
                    "price": price,
                    "seller_id": seller_id,
                    "seller_name": seller_name,
                    "status": "Pending",
                    "transaction_id": transaction_id,
                    "contract_id": contract_id
                })
                
                return True, f"Successfully purchased {product_name} with secure blockchain transaction"

        print("\n❌ Product not found!\n")
        return False, "Product not found"
