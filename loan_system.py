import os
import csv
import uuid
import datetime
from database import Database

class LoanSystem:
    """
    LoanSystem class for handling loan applications, approvals, and repayments.
    This class provides functionality for farmers to apply for loans and admins to approve them.
    """
    
    def __init__(self):
        """Initialize the LoanSystem with necessary file paths."""
        self.loans_file = "loans.csv"
        self.repayments_file = "loan_repayments.csv"
        
        # Ensure the loan files exist with proper headers
        loan_headers = ["loan_id", "farmer_id", "amount", "interest_rate", 
                       "application_date", "status", "approval_date", "due_date"]
        repayment_headers = ["repayment_id", "loan_id", "amount", "date"]
        
        # Initialize files if they don't exist
        data_path = os.path.join("data", self.loans_file)
        if not os.path.exists(data_path):
            Database.write_to_csv(self.loans_file, [], loan_headers)
            
        data_path = os.path.join("data", self.repayments_file)
        if not os.path.exists(data_path):
            Database.write_to_csv(self.repayments_file, [], repayment_headers)

    def apply_for_loan(self, farmer_id, amount, interest_rate):
        """
        Allow a farmer to apply for a loan.
        
        Args:
            farmer_id (str): The ID of the farmer applying for the loan
            amount (float): The amount of the loan
            interest_rate (float): The interest rate of the loan
            
        Returns:
            tuple: (success, message, loan_id if successful)
        """
        if not farmer_id or not amount or amount <= 0:
            return False, "Invalid farmer ID or loan amount", None
        
        # Generate a unique loan ID
        loan_id = str(uuid.uuid4())[:8]
        
        # Get current date
        application_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Set status to Pending
        status = "Pending"
        
        # Set approval date and due date to empty for now
        approval_date = ""
        due_date = ""
        
        # Create a new loan record
        loan_data = [loan_id, farmer_id, amount, interest_rate, 
                     application_date, status, approval_date, due_date]
        
        # Save the loan data to the CSV file using Database class
        try:
            headers = ["loan_id", "farmer_id", "amount", "interest_rate", 
                      "application_date", "status", "approval_date", "due_date"]
            Database.write_to_csv("loans.csv", loan_data, headers)
            return True, f"Loan application submitted successfully! Loan ID: {loan_id}", loan_id
        except Exception as e:
            return False, f"Error applying for loan: {str(e)}", None

    def approve_loan(self, admin_id, loan_id, approved=True):
        """
        Allow an admin to approve or reject a loan application.
        
        Args:
            admin_id (str): The ID of the admin approving the loan
            loan_id (str): The ID of the loan to approve
            approved (bool): Whether to approve or reject the loan
            
        Returns:
            tuple: (success, message)
        """
        # Get all loans with headers
        loans = Database.read_csv_with_headers(self.loans_file)
        
        if not loans:
            return False, "No loan applications found"
            
        try:
            headers = loans[0]  # Save headers
            updated_loans = [headers]  # Start with headers
            found = False
            
            # Process each loan row (skip header)
            for loan in loans[1:]:
                if len(loan) >= 1 and loan[0] == loan_id:
                    found = True
                    
                    # Ensure loan has enough elements
                    while len(loan) < 8:
                        loan.append("")  # Pad with empty strings if needed
                    
                    # If already approved or rejected, return error
                    if loan[5] != "Pending":
                        return False, f"Loan {loan_id} is already {loan[5]}"
                    
                    # Update loan status
                    status = "Approved" if approved else "Rejected"
                    approval_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    
                    # Calculate due date (6 months from approval)
                    due_date = (datetime.datetime.now() + datetime.timedelta(days=180)).strftime("%Y-%m-%d")
                    
                    # Update the loan record
                    loan[5] = status
                    loan[6] = approval_date
                    
                    if approved:
                        loan[7] = due_date
                    
                    updated_loans.append(loan)
                else:
                    updated_loans.append(loan)
            
            if not found:
                return False, f"Loan with ID {loan_id} not found"
            
            # Write the updated loans back to the CSV file
            Database.update_csv_file(self.loans_file, updated_loans)
                
            action = "approved" if approved else "rejected"
            return True, f"Loan {loan_id} has been {action} successfully"
            
        except Exception as e:
            return False, f"Error updating loan status: {str(e)}"

    def make_repayment(self, loan_id, amount):
        """
        Record a loan repayment.
        
        Args:
            loan_id (str): The ID of the loan being repaid
            amount (float): The amount being repaid
            
        Returns:
            tuple: (success, message)
        """
        if not loan_id or not amount or amount <= 0:
            return False, "Invalid loan ID or repayment amount"
        
        # Check if loan exists and is approved
        loans = Database.read_from_csv(self.loans_file)
        loan_exists = False
        loan_approved = False
        
        for loan in loans:
            if len(loan) >= 6 and loan[0] == loan_id:
                loan_exists = True
                if loan[5] == "Approved":
                    loan_approved = True
                break
        
        if not loan_exists:
            return False, f"Loan with ID {loan_id} not found"
        
        if not loan_approved:
            return False, f"Loan with ID {loan_id} is not approved"
        
        # Generate a unique repayment ID
        repayment_id = str(uuid.uuid4())[:8]
        
        # Get current date
        repayment_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Create a new repayment record
        repayment_data = [repayment_id, loan_id, amount, repayment_date]
        
        # Save the repayment data to the CSV file using Database class
        try:
            headers = ["repayment_id", "loan_id", "amount", "date"]
            Database.write_to_csv("loan_repayments.csv", repayment_data, headers)
            return True, f"Repayment of ₱{amount} recorded successfully for loan {loan_id}"
        except Exception as e:
            return False, f"Error recording repayment: {str(e)}"

    def get_farmer_loans(self, farmer_id):
        """
        Get all loans for a specific farmer.
        
        Args:
            farmer_id (str): The ID of the farmer
            
        Returns:
            list: List of loans for the farmer
        """
        # Use the Database class to get loans by farmer ID
        return Database.get_loans_by_farmer(self.loans_file, farmer_id)

    def get_loan_details(self, loan_id):
        """
        Get details for a specific loan.
        
        Args:
            loan_id (str): The ID of the loan
            
        Returns:
            dict: Loan details or None if not found
        """
        # Use the Database class to get the loan by ID
        loan = Database.get_loan_by_id(self.loans_file, loan_id)
        
        if not loan:
            return None
            
        try:
            # Create a dictionary with available data
            loan_dict = {
                "loan_id": loan[0],
            }
            
            # Add other fields if they exist
            if len(loan) > 1:
                loan_dict["farmer_id"] = loan[1]
            if len(loan) > 2:
                loan_dict["amount"] = float(loan[2]) if loan[2] else 0.0
            if len(loan) > 3:
                loan_dict["interest_rate"] = float(loan[3]) if loan[3] else 0.0
            if len(loan) > 4:
                loan_dict["application_date"] = loan[4]
            if len(loan) > 5:
                loan_dict["status"] = loan[5]
            if len(loan) > 6:
                loan_dict["approval_date"] = loan[6]
            if len(loan) > 7:
                loan_dict["due_date"] = loan[7]
                
            return loan_dict
            
        except Exception as e:
            print(f"Error getting loan details: {str(e)}")
            return None

    def get_loan_repayments(self, loan_id):
        """
        Get all repayments for a specific loan.
        
        Args:
            loan_id (str): The ID of the loan
            
        Returns:
            list: List of repayments for the loan
        """
        repayments = Database.read_from_csv(self.repayments_file)
        loan_repayments = []
        
        for repayment in repayments:
            if len(repayment) >= 2 and repayment[1] == loan_id:
                loan_repayments.append(repayment)
        
        return loan_repayments

    def calculate_remaining_balance(self, loan_id):
        """
        Calculate the remaining balance for a loan.
        
        Args:
            loan_id (str): The ID of the loan
            
        Returns:
            tuple: (success, remaining balance or error message)
        """
        loan_details = self.get_loan_details(loan_id)
        
        if not loan_details:
            return False, f"Loan with ID {loan_id} not found"
        
        if loan_details["status"] != "Approved":
            return False, f"Loan with ID {loan_id} is not approved"
        
        # Calculate total amount with interest
        principal = loan_details["amount"]
        interest_rate = loan_details["interest_rate"] / 100  # Convert percentage to decimal
        total_with_interest = principal * (1 + interest_rate)
        
        # Calculate total repayments
        repayments = self.get_loan_repayments(loan_id)
        total_repaid = sum(float(repayment[2]) for repayment in repayments if len(repayment) >= 3)
        
        # Calculate remaining balance
        remaining_balance = total_with_interest - total_repaid
        
        # Ensure balance doesn't go negative
        remaining_balance = max(0, remaining_balance)
        
        return True, remaining_balance

    def get_all_pending_loans(self):
        """
        Get all pending loan applications.
        
        Returns:
            list: List of pending loans
        """
        # Use the Database class to get loans by status
        return Database.get_loans_by_status(self.loans_file, "Pending")

    def generate_loan_report(self):
        """
        Generate a report of all loans.
        
        Returns:
            dict: Report with statistics about loans
        """
        loans = Database.read_from_csv(self.loans_file)
        
        total_loans = len(loans)
        approved_loans = len(Database.get_loans_by_status(self.loans_file, "Approved"))
        pending_loans = len(Database.get_loans_by_status(self.loans_file, "Pending"))
        rejected_loans = len(Database.get_loans_by_status(self.loans_file, "Rejected"))
        
        # Calculate total amount of approved loans
        total_approved_amount = sum(
            float(loan[2]) for loan in loans 
            if len(loan) >= 6 and loan[5] == "Approved" and loan[2].replace('.', '', 1).isdigit()
        )
        
        return {
            "total_loans": total_loans,
            "approved_loans": approved_loans,
            "pending_loans": pending_loans,
            "rejected_loans": rejected_loans,
            "total_approved_amount": total_approved_amount
        }
