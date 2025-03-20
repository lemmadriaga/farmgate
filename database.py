import csv
import os

# Please check if data folders exist 
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
            if not file_exists:
                writer.writerow(headers)  # Write headers if file is new
            writer.writerow(data)

    @staticmethod
    def read_from_csv(filename):
        file_path = os.path.join(DATA_FOLDER, filename)
        if not os.path.isfile(file_path):
            return []

        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            return list(reader)[1:]  # Skip headers
