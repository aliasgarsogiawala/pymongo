"""
Database Initialization Script
Creates collections, indexes, and sample data for the concert booking system
"""
from config import get_database
from datetime import datetime, timedelta
import random

def init_database():
    """Initialize the database with collections, indexes, and sample data"""
    db = get_database()
    
    if db is None:
        print("❌ Failed to connect to database")
        return False
    
    try:
        print("\n🔧 Initializing Concert Booking Database...")
        
        # Create collections if they don't exist
        collections = ['concerts', 'bookings', 'customers']
        
        for collection_name in collections:
            if collection_name not in db.list_collection_names():
                db.create_collection(collection_name)
                print(f"✅ Created collection: {collection_name}")
            else:
                print(f"ℹ️  Collection already exists: {collection_name}")
        
        # Create indexes for better query performance
        print("\n📊 Creating indexes...")
        
        # Concerts indexes
        db.concerts.create_index([('date', 1)])
        db.concerts.create_index([('artist', 1)])
        db.concerts.create_index([('venue', 1)])
        print("✅ Created indexes on concerts collection")
        
        # Bookings indexes
        db.bookings.create_index([('concert_id', 1)])
        db.bookings.create_index([('customer_email', 1)])
        db.bookings.create_index([('booking_date', -1)])
        db.bookings.create_index([('status', 1)])
        print("✅ Created indexes on bookings collection")
        
        # Check if data already exists
        existing_concerts = db.concerts.count_documents({})
        
        if existing_concerts > 0:
            print(f"\nℹ️  Database already has {existing_concerts} concerts. Skipping sample data insertion.")
            print("✅ Database initialization complete!")
            return True
        
        # Insert sample concerts
        print("\n🎵 Inserting sample concert data...")
        
        sample_concerts = [
            {
                'name': 'Bollywood Nights Mumbai',
                'artist': 'Arijit Singh',
                'venue': 'Jio Garden, Mumbai',
                'date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                'time': '19:00',
                'ticket_price': 8500.00,  # ₹8,500
                'total_seats': 500,
                'available_seats': 500,
                'genre': 'Bollywood',
                'description': 'Magical evening with Bollywood\'s most beloved playback singer',
                'created_at': datetime.now()
            },
            {
                'name': 'Classical Raag Darbar',
                'artist': 'Ustad Zakir Hussain',
                'venue': 'Nehru Centre, Mumbai',
                'date': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
                'time': '20:00',
                'ticket_price': 6000.00,  # ₹6,000
                'total_seats': 200,
                'available_seats': 200,
                'genre': 'Classical',
                'description': 'Mesmerizing tabla performance by the legendary maestro',
                'created_at': datetime.now()
            },
            {
                'name': 'Punjabi Folk Festival',
                'artist': 'Diljit Dosanjh',
                'venue': 'Thyagaraj Stadium, Delhi',
                'date': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'),
                'time': '18:30',
                'ticket_price': 12000.00,  # ₹12,000
                'total_seats': 1000,
                'available_seats': 1000,
                'genre': 'Punjabi',
                'description': 'High-energy Punjabi music and dance celebration',
                'created_at': datetime.now()
            },
            {
                'name': 'Carnatic Music Concert',
                'artist': 'T.M. Krishna',
                'venue': 'Music Academy, Chennai',
                'date': (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'),
                'time': '18:00',
                'ticket_price': 4500.00,  # ₹4,500
                'total_seats': 300,
                'available_seats': 300,
                'genre': 'Carnatic',
                'description': 'Traditional South Indian classical music performance',
                'created_at': datetime.now()
            },
            {
                'name': 'Sufi Night Bangalore',
                'artist': 'Kailash Kher',
                'venue': 'Palace Grounds, Bangalore',
                'date': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
                'time': '19:30',
                'ticket_price': 7500.00,  # ₹7,500
                'total_seats': 400,
                'available_seats': 400,
                'genre': 'Sufi',
                'description': 'Soulful Sufi music that touches the heart and soul',
                'created_at': datetime.now()
            },
            {
                'name': 'Indie Rock Kolkata',
                'artist': 'Parikrama',
                'venue': 'Netaji Indoor Stadium, Kolkata',
                'date': (datetime.now() + timedelta(days=50)).strftime('%Y-%m-%d'),
                'time': '20:00',
                'ticket_price': 5500.00,  # ₹5,500
                'total_seats': 600,
                'available_seats': 600,
                'genre': 'Rock',
                'description': 'India\'s premier rock band performing their greatest hits',
                'created_at': datetime.now()
            }
        ]
        
        result = db.concerts.insert_many(sample_concerts)
        print(f"✅ Inserted {len(result.inserted_ids)} sample concerts")
        
        # Insert sample bookings
        print("\n🎟️  Creating sample bookings...")
        
        concerts = list(db.concerts.find())
        sample_customers = [
            {'name': 'Rajesh Kumar', 'email': 'rajesh.kumar@example.com', 'phone': '+91-9876543210'},
            {'name': 'Priya Sharma', 'email': 'priya.sharma@example.com', 'phone': '+91-9876543211'},
            {'name': 'Amit Patel', 'email': 'amit.patel@example.com', 'phone': '+91-9876543212'},
            {'name': 'Sneha Reddy', 'email': 'sneha.reddy@example.com', 'phone': '+91-9876543213'},
            {'name': 'Vikram Singh', 'email': 'vikram.singh@example.com', 'phone': '+91-9876543214'},
        ]
        
        sample_bookings = []
        for i, concert in enumerate(concerts[:4]):  # Create bookings for first 4 concerts
            customer = sample_customers[i % len(sample_customers)]
            num_tickets = random.randint(2, 5)
            
            booking = {
                'concert_id': str(concert['_id']),
                'customer_name': customer['name'],
                'customer_email': customer['email'],
                'customer_phone': customer['phone'],
                'num_tickets': num_tickets,
                'ticket_price': concert['ticket_price'],
                'total_amount': concert['ticket_price'] * num_tickets,
                'booking_date': datetime.now() - timedelta(days=random.randint(1, 10)),
                'status': random.choice(['confirmed', 'confirmed', 'confirmed', 'pending'])
            }
            sample_bookings.append(booking)
            
            # Update available seats
            db.concerts.update_one(
                {'_id': concert['_id']},
                {'$inc': {'available_seats': -num_tickets}}
            )
        
        if sample_bookings:
            result = db.bookings.insert_many(sample_bookings)
            print(f"✅ Inserted {len(result.inserted_ids)} sample bookings")
        
        print("\n✅ Database initialization complete!")
        print(f"📊 Total Concerts: {db.concerts.count_documents({})}")
        print(f"🎟️  Total Bookings: {db.bookings.count_documents({})}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        return False

if __name__ == '__main__':
    init_database()
