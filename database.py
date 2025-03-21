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

        try:
            with open(file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                
                if not file_exists or os.stat(file_path).st_size == 0:
                    print("\n🔍 DEBUG: Writing headers to CSV...", headers)
                    writer.writerow(headers)
                
                print("\n🔍 DEBUG: Writing user data to CSV...", data)
                writer.writerow(data)
                print("\n✅ DEBUG: Data successfully written to CSV.")
        except Exception as e:
            print("\n❌ ERROR: Could not write to CSV file:", e)
