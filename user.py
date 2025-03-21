import hashlib
import uuid
from database import Database

class User:
    """
    Base User class that serves as the parent class for Farmer, Buyer, and Admin.
    Implements common functionality like registration, login, and profile management.
    """
    def __init__(self, user_id=None, name=None, email=None, password=None, role=None):
        self.user_id = user_id if user_id else str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.password = password  # This should be the hashed password
        self.role = role
        self.users_file = "users.csv"
        self.headers = ["user_id", "username", "password", "role", "email"]

    def hash_password(self, password):
        """Hash a password for security."""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_input(self, username, password, role, email):
        """Validate user input for registration."""
        if not all([username, password, role, email]):
            return False, "All fields are required"
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        if role not in ["farmer", "buyer", "admin"]:
            return False, "Invalid role. Must be farmer, buyer, or admin"
        if "@" not in email or "." not in email:
            return False, "Invalid email format"
        return True, "Valid input"

    def check_existing_user(self, username):
        """Check if a username already exists in the database."""
        users = Database.read_from_csv(self.users_file)
        return any(user[1] == username for user in users)

    def register(self, username, password, role, email):
        """
        Register a new user in the system.
        Returns a tuple (success, message)
        """
        print("\n🔍 Starting registration process...")

        # Validate input
        is_valid, message = self.validate_input(username, password, role, email)
        if not is_valid:
            print(f"\n❌ Validation failed: {message}")
            return False, message

        # Check if username exists
        if self.check_existing_user(username):
            print("\n❌ Username already exists")
            return False, "Username already exists"

        # Create new user
        user_id = str(uuid.uuid4())[:8]
        hashed_password = self.hash_password(password)
        user_data = [user_id, username, hashed_password, role, email]

        print("\n🔍 Attempting to save user data...")

        try:
            Database.write_to_csv(self.users_file, user_data, self.headers)
            print("\n✅ User successfully registered!")
            
            # Update the current instance with the new data
            self.user_id = user_id
            self.name = username
            self.email = email
            self.password = hashed_password
            self.role = role
            
            return True, f"Registration successful! Your User ID: {user_id}"
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return False, "An error occurred while saving user data."

    def login(self, username, password):
        """
        Authenticate a user with username and password.
        Returns a tuple (success, user_details or error_message)
        """
        users = Database.read_from_csv(self.users_file)
        hashed_input_password = self.hash_password(password)

        for user in users:
            if user[1] == username and user[2] == hashed_input_password:
                # Update the current instance with user data
                self.user_id = user[0]
                self.name = username
                self.email = user[4]
                self.password = user[2]  # Hashed password
                self.role = user[3]
                
                user_details = {
                    "user_id": user[0],
                    "username": username,
                    "role": user[3],
                    "email": user[4]
                }
                
                return True, user_details
                
        return False, "Invalid username or password"

    def updateProfile(self, field, new_value):
        """
        Update a specific field in the user's profile.
        Supported fields: username, email, password
        Returns a tuple (success, message)
        """
        if not self.user_id:
            return False, "User not logged in"
            
        if field not in ["username", "email", "password"]:
            return False, f"Cannot update field: {field}"
            
        users = Database.read_from_csv(self.users_file)
        updated_users = []
        found = False
        
        for user in users:
            if user[0] == self.user_id:
                found = True
                
                # Handle different field updates
                if field == "username":
                    # Check if new username already exists
                    if any(u[1] == new_value and u[0] != self.user_id for u in users):
                        return False, "Username already exists"
                    user[1] = new_value
                    self.name = new_value
                    
                elif field == "email":
                    # Validate email format
                    if "@" not in new_value or "." not in new_value:
                        return False, "Invalid email format"
                    user[4] = new_value
                    self.email = new_value
                    
                elif field == "password":
                    # Validate password length
                    if len(new_value) < 6:
                        return False, "Password must be at least 6 characters long"
                    hashed_password = self.hash_password(new_value)
                    user[2] = hashed_password
                    self.password = hashed_password
                    
            updated_users.append(user)
            
        if not found:
            return False, "User not found"
            
        try:
            # Write updated data back to CSV
            with open(f"data/{self.users_file}", mode='w', newline='') as file:
                import csv
                writer = csv.writer(file)
                writer.writerow(self.headers)
                writer.writerows(updated_users)
                
            return True, f"Successfully updated {field}"
        except Exception as e:
            return False, f"Error updating profile: {e}"

    def get_user_details(self):
        """Return the current user's details as a dictionary."""
        if not self.user_id:
            return None
            
        return {
            "user_id": self.user_id,
            "username": self.name,
            "role": self.role,
            "email": self.email
        }
