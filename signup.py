import os
import hashlib
import uuid
from database import Database

class Signup:
    def __init__(self):
        self.users_file = "users.csv"
        self.headers = ["user_id", "username", "password", "role", "email"]

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_input(self, username, password, role, email):
        if not all([username, password, role, email]):
            return False, "All fields are required"
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        if role not in ["farmer", "buyer", "admin"]:
            return False, "Invalid role"
        if "@" not in email or "." not in email:
            return False, "Invalid email format"
        return True, "Valid input"

    def check_existing_user(self, username):
        users = Database.read_from_csv(self.users_file)
        return any(user[1] == username for user in users)

    def register_user(self, username, password, role, email):
        print("\n🔍 DEBUG: Starting registration process...")

        is_valid, message = self.validate_input(username, password, role, email)
        if not is_valid:
            print("\n DEBUG: Validation failed:", message)
            return False, message

        if self.check_existing_user(username):
            print("\n DEBUG: Username already exists")
            return False, "Username already exists"

        user_id = str(uuid.uuid4())[:8]
        hashed_password = self.hash_password(password)
        user_data = [user_id, username, hashed_password, role, email]

        print("\n🔍 DEBUG: Attempting to write user data to CSV...", user_data)

        try:
            Database.write_to_csv(self.users_file, user_data, self.headers)
            print("\n✅ DEBUG: User successfully saved.")
            return True, f"Registration successful! Your User ID: {user_id}"
        except Exception as e:
            print("\n ERROR: Failed to write to CSV:", e)
            return False, "An error occurred while saving user data."


