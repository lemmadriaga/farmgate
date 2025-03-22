import os
import csv
from database import Database

class EducationalHub:
    """
    EducationalHub class for providing educational resources to farmers and buyers.
    This class manages educational content related to farming, market trends, and best practices.
    """
    
    def __init__(self):
        """Initialize the EducationalHub with necessary file paths."""
        self.resources_file = "educational_resources.csv"
        
        # Ensure the resources file exists with proper headers
        resource_headers = ["resource_id", "title", "category", "content", "tags", "date_added"]
        
        # Initialize file if it doesn't exist
        data_path = os.path.join("data", self.resources_file)
        if not os.path.exists(data_path):
            self._initialize_default_resources(resource_headers)
    
    def _initialize_default_resources(self, headers):
        """Initialize the resources file with default educational content."""
        default_resources = [
            ["res001", "Sustainable Farming Practices", "Farming", 
             "Learn about sustainable farming practices that can improve soil health and crop yield while reducing environmental impact.",
             "sustainable,farming,environment", "2025-03-21"],
            ["res002", "Understanding Market Trends", "Market", 
             "This guide helps farmers understand market trends and price fluctuations to maximize profits.",
             "market,prices,trends", "2025-03-21"],
            ["res003", "Loan Management for Farmers", "Finance", 
             "Tips for managing farm loans effectively, including repayment strategies and avoiding debt traps.",
             "loans,finance,management", "2025-03-21"],
            ["res004", "Organic Certification Process", "Certification", 
             "Step-by-step guide to obtaining organic certification for your farm products.",
             "organic,certification,standards", "2025-03-21"],
            ["res005", "Effective Irrigation Techniques", "Farming", 
             "Modern irrigation techniques that conserve water while ensuring optimal crop growth.",
             "irrigation,water,conservation", "2025-03-21"]
        ]
        
        # Write default resources to the file
        for resource in default_resources:
            Database.write_to_csv(self.resources_file, resource, headers)
    
    def view_all_resources(self):
        """View all educational resources available in the system."""
        resources = Database.read_from_csv(self.resources_file)
        
        if not resources:
            print("\n No educational resources found.\n")
            return []
        
        print("\n===== Educational Resources =====\n")
        for resource in resources:
            if len(resource) >= 3:
                resource_id = resource[0]
                title = resource[1]
                category = resource[2]
                
                print(f"ID: {resource_id}")
                print(f"Title: {title}")
                print(f"Category: {category}")
                print("\n----------------------------\n")
        
        return resources
    
    def search_resources(self, query):
        """
        Search for educational resources by title, category, or tags.
        
        Args:
            query (str): The search query
            
        Returns:
            list: List of resources matching the query
        """
        resources = Database.read_from_csv(self.resources_file)
        query = query.lower()
        
        # Search in title, category, and tags
        matching_resources = []
        for resource in resources:
            if len(resource) >= 5:
                title = resource[1].lower()
                category = resource[2].lower()
                tags = resource[4].lower()
                
                if query in title or query in category or query in tags:
                    matching_resources.append(resource)
        
        if not matching_resources:
            print(f"\n No resources found matching '{query}'.\n")
            return []
        
        print(f"\n===== Search Results for '{query}' =====\n")
        for resource in matching_resources:
            resource_id = resource[0]
            title = resource[1]
            category = resource[2]
            
            print(f"ID: {resource_id}")
            print(f"Title: {title}")
            print(f"Category: {category}")
            print("\n----------------------------\n")
        
        return matching_resources
    
    def view_resource_details(self, resource_id):
        """
        View detailed information about a specific educational resource.
        
        Args:
            resource_id (str): The ID of the resource to view
            
        Returns:
            dict: Resource details or None if not found
        """
        resources = Database.read_from_csv(self.resources_file)
        
        for resource in resources:
            if len(resource) >= 1 and resource[0] == resource_id:
                print("\n===== Resource Details =====\n")
                
                resource_id = resource[0]
                title = resource[1] if len(resource) > 1 else "Unknown"
                category = resource[2] if len(resource) > 2 else "Unknown"
                content = resource[3] if len(resource) > 3 else "No content available"
                tags = resource[4] if len(resource) > 4 else "No tags"
                date_added = resource[5] if len(resource) > 5 else "Unknown"
                
                print(f"ID: {resource_id}")
                print(f"Title: {title}")
                print(f"Category: {category}")
                print(f"Date Added: {date_added}")
                print(f"Tags: {tags}")
                print("\nContent:")
                print(f"{content}")
                print("\n----------------------------\n")
                
                return {
                    "resource_id": resource_id,
                    "title": title,
                    "category": category,
                    "content": content,
                    "tags": tags,
                    "date_added": date_added
                }
        
        print(f"\n Resource with ID '{resource_id}' not found.\n")
        return None
    
    def add_resource(self, title, category, content, tags):
        """
        Add a new educational resource to the system.
        
        Args:
            title (str): The title of the resource
            category (str): The category of the resource
            content (str): The content of the resource
            tags (str): Comma-separated tags for the resource
            
        Returns:
            tuple: (success, message, resource_id if successful)
        """
        if not title or not category or not content:
            return False, "Title, category, and content are required", None
        
        # Generate a unique resource ID
        import uuid
        resource_id = "res" + str(uuid.uuid4())[:5]
        
        # Get current date
        import datetime
        date_added = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Create a new resource record
        resource_data = [resource_id, title, category, content, tags, date_added]
        
        # Save the resource data to the CSV file
        try:
            headers = ["resource_id", "title", "category", "content", "tags", "date_added"]
            Database.write_to_csv(self.resources_file, resource_data, headers)
            return True, f"Resource '{title}' added successfully! Resource ID: {resource_id}", resource_id
        except Exception as e:
            return False, f"Error adding resource: {str(e)}", None
    
    def get_resources_by_category(self, category):
        """
        Get all resources in a specific category.
        
        Args:
            category (str): The category to filter by
            
        Returns:
            list: List of resources in the specified category
        """
        resources = Database.read_from_csv(self.resources_file)
        category_resources = []
        
        for resource in resources:
            if len(resource) >= 3 and resource[2].lower() == category.lower():
                category_resources.append(resource)
        
        if not category_resources:
            print(f"\n No resources found in category '{category}'.\n")
            return []
        
        print(f"\n===== Resources in Category '{category}' =====\n")
        for resource in category_resources:
            resource_id = resource[0]
            title = resource[1]
            
            print(f"ID: {resource_id}")
            print(f"Title: {title}")
            print("\n----------------------------\n")
        
        return category_resources
    
    def get_latest_resources(self, limit=5):
        """
        Get the latest educational resources added to the system.
        
        Args:
            limit (int): Maximum number of resources to return
            
        Returns:
            list: List of the latest resources
        """
        resources = Database.read_from_csv(self.resources_file)
        
        # Sort resources by date (assuming date is in the 6th column)
        sorted_resources = sorted(
            resources, 
            key=lambda x: x[5] if len(x) > 5 else "0000-00-00", 
            reverse=True
        )
        
        # Limit the number of resources
        latest_resources = sorted_resources[:limit]
        
        if not latest_resources:
            print("\n No resources found.\n")
            return []
        
        print(f"\n===== Latest Educational Resources =====\n")
        for resource in latest_resources:
            resource_id = resource[0]
            title = resource[1] if len(resource) > 1 else "Unknown"
            category = resource[2] if len(resource) > 2 else "Unknown"
            date_added = resource[5] if len(resource) > 5 else "Unknown"
            
            print(f"ID: {resource_id}")
            print(f"Title: {title}")
            print(f"Category: {category}")
            print(f"Date Added: {date_added}")
            print("\n----------------------------\n")
        
        return latest_resources
