from database import Database

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
