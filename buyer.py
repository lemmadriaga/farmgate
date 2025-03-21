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
        products = Database.read_from_csv("marketplace.csv")
        for product in products:
            if product[0] == product_id:
                # Record transaction with buyer ID
                transaction_data = [self.user_id, self.name, product[2], product[3], "Pending"]
                Database.write_to_csv("transactions.csv", transaction_data, 
                                    ["Buyer ID", "Buyer Name", "Product", "Price", "Status"])
                
                # Add to purchase history
                self.purchase_history.append({
                    "product_name": product[2],
                    "price": product[3],
                    "seller_id": product[0],
                    "seller_name": product[1],
                    "status": "Pending"
                })
                
                print(f"\n✅ {self.name} purchased {product[2]} for ₱{product[3]}!\n")
                return True, f"Successfully purchased {product[2]}"

        print("\n❌ Product not found!\n")
        return False, "Product not found"
