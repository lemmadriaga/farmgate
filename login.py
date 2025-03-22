from database import Database
import hashlib

class Login:
    def __init__(self):
        self.users_file = "users.csv"

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate_user(self, username, password):
        users = Database.read_from_csv(self.users_file)
        hashed_input_password = self.hash_password(password)

        for user in users:
            if user[1] == username and user[2] == hashed_input_password:
                return True
        return False

    def get_user_details(self, username):
        users = Database.read_from_csv(self.users_file)
        for user in users:
            if user[1] == username:
                print("\n🔍 DEBUG: Retrieved user details:", user)  # Debugging line
                return {"user_id": user[0], "role": user[3]}
        print("\n DEBUG: User not found in users.csv")
        return None

