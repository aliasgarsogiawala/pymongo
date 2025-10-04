"""
Configuration file for MongoDB connection and application settings.
"""
import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('.env.local')

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('MONGO_DB', 'concert_billing')

def get_database():
    """
    Create and return MongoDB database connection.
    """
    try:
        if not MONGO_URI:
            raise ValueError("MONGO_URI not found in environment variables")
        
        # Create MongoDB client with Atlas URI
        client = MongoClient(
            MONGO_URI, 
            serverSelectionTimeoutMS=30000,
            tlsAllowInvalidCertificates=True
        )
        
        # Get database
        database = client[DATABASE_NAME]
        
        # Test connection
        client.admin.command('ping')
        print(f"✅ Successfully connected to MongoDB Atlas database: {DATABASE_NAME}")
        
        return database
    
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {str(e)}")
        print("💡 Tips to fix connection issues:")
        print("   1. Check if your IP is whitelisted in MongoDB Atlas Network Access")
        print("   2. Verify username/password in the connection string")
        print("   3. Ensure the database user has proper permissions")
        print("   4. SSL/TLS handshake issue - check OpenSSL version")
        print("\n⚠️  Note: The application is ready to run. If you can fix the MongoDB")
        print("    connection (IP whitelist, credentials), the app will work correctly.")
        return None

# Collections
CONCERTS_COLLECTION = 'concerts'
CUSTOMERS_COLLECTION = 'customers'
BOOKINGS_COLLECTION = 'bookings'
TICKETS_COLLECTION = 'tickets'
INVOICES_COLLECTION = 'invoices'