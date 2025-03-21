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
    def read_from_csv(filename):  # ✅ Ensure this method exists
        file_path = os.path.join(DATA_FOLDER, filename)
        if not os.path.isfile(file_path):
            return []

        with open(file_path, mode='r', newline='') as file:
            reader = list(csv.reader(file))
            if len(reader) < 2:
                return []
            return reader[1:]
