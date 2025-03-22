from database import Database
from blockchain import Blockchain
import uuid

class Marketplace:
    @staticmethod
    def display_products():
        products = Database.read_from_csv("marketplace.csv")
        if not products:
            print("\n No products available in the marketplace.\n")
        else:
            print("\n Marketplace Listings:")
            for product in products:
                print(f"- {product[2]} | ₱{product[3]} | Seller: {product[1]} | ID: {product[0]}")
            print()
    
    @staticmethod
    def add_product(farmer_id, farmer_name, product_name, price):
        """Add a product to the marketplace with blockchain integration"""
        # Generate a unique product ID
        product_id = str(uuid.uuid4())[:8]
        
        # Add to traditional CSV storage
        product = [product_id, farmer_id, product_name, price]
        Database.write_to_csv("marketplace.csv", product, ["Product ID", "Farmer ID", "Product Name", "Price"])
        
        # Store in blockchain
        blockchain = Blockchain()
        success, message = blockchain.store_product_listing(product_id, farmer_id, product_name, price)
        
        if success:
            print(f"\n {product_name} listed for ₱{float(price):.2f} by {farmer_name}!")
            print(f"   Product ID: {product_id} (secured by blockchain)\n")
        else:
            print(f"\n⚠️ {product_name} listed in traditional system only.")
            print(f"   Product ID: {product_id}\n")
        
        return product_id
    
    @staticmethod
    def get_product_details(product_id):
        """Get details of a specific product"""
        products = Database.read_from_csv("marketplace.csv")
        for product in products:
            if product[0] == product_id:
                return {
                    "product_id": product[0],
                    "farmer_id": product[1],
                    "product_name": product[2],
                    "price": float(product[3]) if isinstance(product[3], str) else product[3]
                }
        return None
