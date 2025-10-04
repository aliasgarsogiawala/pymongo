"""
Simple connection test for MongoDB Atlas
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

def test_connection():
    """Test different connection methods to MongoDB Atlas"""
    uri = os.getenv('MONGO_URI')
    
    if not uri:
        print("❌ MONGO_URI not found in environment")
        return
    
    print(f"🔗 Testing connection to: {uri[:50]}...")
    
    # Method 1: Basic connection
    try:
        print("\n📡 Method 1: Basic connection...")
        client = MongoClient(uri)
        client.admin.command('ping')
        print("✅ Basic connection successful!")
        client.close()
        return True
    except Exception as e:
        print(f"❌ Basic connection failed: {str(e)[:200]}...")
    
    # Method 2: With SSL disabled (for testing)
    try:
        print("\n📡 Method 2: Connection with SSL settings...")
        client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
        client.admin.command('ping')
        print("✅ SSL connection successful!")
        client.close()
        return True
    except Exception as e:
        print(f"❌ SSL connection failed: {str(e)[:200]}...")
    
    # Method 3: Parse URI and show details
    print(f"\n📋 Connection string details:")
    print(f"   Full URI: {uri}")
    
    if "mongodb+srv://" in uri:
        # Extract components
        parts = uri.replace("mongodb+srv://", "").split("@")
        if len(parts) == 2:
            credentials = parts[0]
            cluster_info = parts[1]
            print(f"   Credentials: {credentials[:10]}...")
            print(f"   Cluster: {cluster_info}")
    
    print("\n💡 Troubleshooting steps:")
    print("   1. Verify your MongoDB Atlas cluster is running")
    print("   2. Check Network Access - whitelist 0.0.0.0/0 (anywhere) for testing")
    print("   3. Verify Database Access user exists and has readWrite permissions")
    print("   4. Check if your connection string is correct from Atlas Connect button")
    
    return False

if __name__ == "__main__":
    test_connection()