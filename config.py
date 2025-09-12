"""
Configuration file for MongoDB connection and application settings.
"""
import os
from pymongo import MongoClient

# MongoDB Configuration
MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost')
MONGODB_PORT = int(os.getenv('MONGODB_PORT', 27017))
DATABASE_NAME = os.getenv('DATABASE_NAME', 'concert_billing')

def get_database():
    """
    Create and return MongoDB database connection.
    """
    try:
        # Create MongoDB client
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        
        # Get database
        database = client[DATABASE_NAME]
        
        # Test connection
        client.admin.command('ping')
        print(f"Successfully connected to MongoDB database: {DATABASE_NAME}")
        
        return database
    
    except Exception as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
        return None

# Collections
CONCERTS_COLLECTION = 'concerts'
CUSTOMERS_COLLECTION = 'customers'
BOOKINGS_COLLECTION = 'bookings'
TICKETS_COLLECTION = 'tickets'
INVOICES_COLLECTION = 'invoices'