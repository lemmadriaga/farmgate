from database import Database
import uuid

class Farmer:
    def __init__(self, name, contact_info):
        self.farmer_id = str(uuid.uuid4())[:8]
        self.name = name
        self.contact_info = contact_info

    def list_produce(self, product_name, price):
        product = [self.farmer_id, self.name, product_name, price]
        Database.write_to_csv("marketplace.csv", product, ["Farmer ID", "Name", "Product", "Price"])
        print(f"\n✅ {product_name} listed for ₱{price:.2f} by {self.name}!\n")

    @staticmethod
    def get_farmers():
        return Database.read_from_csv("farmers.csv")
