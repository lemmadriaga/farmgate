from database import Database
import uuid

class Buyer:
    def __init__(self, name, contact_info):
        self.buyer_id = str(uuid.uuid4())[:8]
        self.name = name
        self.contact_info = contact_info

    def purchase_produce(self, product_id):
        products = Database.read_from_csv("marketplace.csv")
        for product in products:
            if product[0] == product_id:
                Database.write_to_csv("transactions.csv", [self.name, product[2], product[3]], ["Buyer", "Product", "Price"])
                print(f"\n {self.name} purchased {product[2]} for ₱{product[3]}!\n")
                return

        print("\n Product not found!\n")
