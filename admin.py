class Admin:
    def __init__(self, name):
        self.name = name

    def approve_transaction(self, buyer_name, product_name):
        print(f"\n Admin {self.name} approved {buyer_name}'s purchase of {product_name}!\n")
