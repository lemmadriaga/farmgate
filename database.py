import csv
import os

DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

class Database:
    @staticmethod
    def write_to_csv(filename, data, headers):
        file_path = os.path.join(DATA_FOLDER, filename)
        file_exists = os.path.isfile(file_path)

        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists or os.stat(file_path).st_size == 0:
                writer.writerow(headers)
            writer.writerow(data)

    @staticmethod
    def read_from_csv(filename):
        """Read data from CSV file, skipping the header row"""
        file_path = os.path.join(DATA_FOLDER, filename)
        if not os.path.isfile(file_path):
            return []

        with open(file_path, mode='r', newline='') as file:
            reader = list(csv.reader(file))
            if len(reader) < 2:
                return []
            return reader[1:]
            
    @staticmethod
    def read_csv_with_headers(filename):
        """Read data from CSV file, including the header row"""
        file_path = os.path.join(DATA_FOLDER, filename)
        if not os.path.isfile(file_path):
            return []

        with open(file_path, mode='r', newline='') as file:
            reader = list(csv.reader(file))
            return reader
    
    @staticmethod
    def update_csv_file(filename, data):
        """Update an entire CSV file with new data (including headers)"""
        file_path = os.path.join(DATA_FOLDER, filename)
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
            
    @staticmethod
    def get_loans_by_status(filename, status):
        """Get all loans with a specific status"""
        loans = Database.read_from_csv(filename)
        return [loan for loan in loans if len(loan) >= 6 and loan[5] == status]
    
    @staticmethod
    def get_loans_by_farmer(filename, farmer_id):
        """Get all loans for a specific farmer"""
        loans = Database.read_from_csv(filename)
        return [loan for loan in loans if len(loan) >= 2 and loan[1] == farmer_id]
    
    @staticmethod
    def get_loan_by_id(filename, loan_id):
        """Get a specific loan by ID"""
        loans = Database.read_from_csv(filename)
        for loan in loans:
            if len(loan) >= 1 and loan[0] == loan_id:
                return loan
        return None
