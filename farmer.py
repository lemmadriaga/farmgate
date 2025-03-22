from database import Database
import uuid
from user import User
from loan_system import LoanSystem

class Farmer(User):
    def __init__(self, name, contact_info=None, user_id=None, email=None, password=None):
        # Call the parent class constructor
        super().__init__(user_id=user_id, name=name, email=email, password=password, role="farmer")
        self.contact_info = contact_info
        self.farm_location = None
        self.products = []

    def list_produce(self, product_name, price):
        # Use the Marketplace class to add the product with blockchain integration
        from marketplace import Marketplace
        product_id = Marketplace.add_product(self.user_id, self.name, product_name, price)
        
        # Add to farmer's products list
        self.products.append({"id": product_id, "name": product_name, "price": price})

    @staticmethod
    def get_farmers():
        return Database.read_from_csv("farmers.csv")
        
    def set_farm_location(self, location):
        """Set the location of the farmer's farm"""
        self.farm_location = location
        return True
        
    def apply_for_loan(self, loan_amount, interest_rate):
        """Apply for a loan through the LoanSystem"""
        # Create a LoanSystem instance
        loan_system = LoanSystem()
        
        # Apply for the loan using the LoanSystem
        success, message, loan_id = loan_system.apply_for_loan(
            farmer_id=self.user_id,
            amount=loan_amount,
            interest_rate=interest_rate
        )
        
        if success:
            print(f"\n✅ {message}\n")
        else:
            print(f"\n {message}\n")
            
        return success, message
        
    def view_my_loans(self):
        """View all loans applied for by this farmer"""
        loan_system = LoanSystem()
        farmer_loans = loan_system.get_farmer_loans(self.user_id)
        
        if not farmer_loans:
            print("\n No loans found for your account.\n")
            return []
        
        print("\n===== Your Loan Applications =====\n")
        for loan in farmer_loans:
            if len(loan) >= 6:
                loan_id = loan[0]
                amount = loan[2]
                interest_rate = loan[3]
                application_date = loan[4]
                status = loan[5]
                
                print(f"Loan ID: {loan_id}")
                print(f"Amount: ₱{amount}")
                print(f"Interest Rate: {interest_rate}%")
                print(f"Application Date: {application_date}")
                print(f"Status: {status}")
                
                # If loan is approved, show due date and remaining balance
                if status == "Approved" and len(loan) >= 8:
                    approval_date = loan[6]
                    due_date = loan[7]
                    print(f"Approval Date: {approval_date}")
                    print(f"Due Date: {due_date}")
                    
                    # Calculate remaining balance
                    success, result = loan_system.calculate_remaining_balance(loan_id)
                    if success:
                        print(f"Remaining Balance: ₱{result:.2f}")
                
                print("\n----------------------------\n")
        
        return farmer_loans
    
    def make_loan_repayment(self, loan_id, amount):
        """Make a repayment on an existing loan"""
        loan_system = LoanSystem()
        
        # First check if this loan belongs to the farmer
        farmer_loans = loan_system.get_farmer_loans(self.user_id)
        loan_belongs_to_farmer = False
        
        for loan in farmer_loans:
            if len(loan) >= 1 and loan[0] == loan_id:
                loan_belongs_to_farmer = True
                break
        
        if not loan_belongs_to_farmer:
            print("\n This loan does not belong to you or does not exist.\n")
            return False, "This loan does not belong to you or does not exist."
        
        # Make the repayment
        success, message = loan_system.make_repayment(loan_id, amount)
        
        if success:
            print(f"\n✅ {message}\n")
        else:
            print(f"\n {message}\n")
            
        return success, message
