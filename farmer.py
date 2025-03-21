from database import Database
import uuid
from user import User

class Farmer(User):
    def __init__(self, name, contact_info=None, user_id=None, email=None, password=None):
        # Call the parent class constructor
        super().__init__(user_id=user_id, name=name, email=email, password=password, role="farmer")
        self.contact_info = contact_info
        self.farm_location = None
        self.products = []

    def list_produce(self, product_name, price):
        product = [self.user_id, self.name, product_name, price]
        Database.write_to_csv("marketplace.csv", product, ["Farmer ID", "Name", "Product", "Price"])
        print(f"\n✅ {product_name} listed for ₱{price:.2f} by {self.name}!\n")
        
        # Add to farmer's products list
        self.products.append({"name": product_name, "price": price})

    @staticmethod
    def get_farmers():
        return Database.read_from_csv("farmers.csv")
        
    def set_farm_location(self, location):
        """Set the location of the farmer's farm"""
        self.farm_location = location
        return True
        
    def apply_for_loan(self, loan_amount, interest_rate):
        """Apply for a loan through the system"""
        loan_data = {
            "farmer_id": self.user_id,
            "farmer_name": self.name,
            "amount": loan_amount,
            "interest_rate": interest_rate,
            "status": "Pending"
        }
        
        try:
            Database.write_to_csv("loans.csv", 
                                [loan_data["farmer_id"], loan_data["farmer_name"], 
                                 loan_data["amount"], loan_data["interest_rate"], loan_data["status"]], 
                                ["Farmer ID", "Farmer Name", "Amount", "Interest Rate", "Status"])
            print(f"\n✅ Loan application for ₱{loan_amount:.2f} submitted successfully!\n")
            return True, "Loan application submitted successfully!"
        except Exception as e:
            print(f"\n❌ Error applying for loan: {e}\n")
            return False, f"Error applying for loan: {e}"
