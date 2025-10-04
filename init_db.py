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
                'name': 'Summer Rock Festival 2025',
                'artist': 'The Rock Legends',
                'venue': 'Madison Square Garden',
                'date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                'time': '19:00',
                'ticket_price': 125.00,
                'total_seats': 500,
                'available_seats': 500,
                'genre': 'Rock',
                'description': 'An epic night of rock music featuring legendary performers',
                'created_at': datetime.now()
            },
            {
                'name': 'Jazz Night Under Stars',
                'artist': 'The Smooth Jazz Quartet',
                'venue': 'Blue Note Jazz Club',
                'date': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
                'time': '20:00',
                'ticket_price': 85.00,
                'total_seats': 200,
                'available_seats': 200,
                'genre': 'Jazz',
                'description': 'Intimate jazz performance in a cozy club setting',
                'created_at': datetime.now()
            },
            {
                'name': 'Electronic Dance Extravaganza',
                'artist': 'DJ Pulse & Friends',
                'venue': 'Electric Arena',
                'date': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'),
                'time': '21:00',
                'ticket_price': 95.00,
                'total_seats': 1000,
                'available_seats': 1000,
                'genre': 'Electronic',
                'description': 'All-night EDM party with top international DJs',
                'created_at': datetime.now()
            },
            {
                'name': 'Classical Symphony Evening',
                'artist': 'Metropolitan Orchestra',
                'venue': 'Concert Hall',
                'date': (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'),
                'time': '18:30',
                'ticket_price': 150.00,
                'total_seats': 300,
                'available_seats': 300,
                'genre': 'Classical',
                'description': 'Beautiful classical music performed by world-class musicians',
                'created_at': datetime.now()
            },
            {
                'name': 'Hip Hop Showcase 2025',
                'artist': 'MC Flow & The Beat Squad',
                'venue': 'Urban Stage',
                'date': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
                'time': '20:30',
                'ticket_price': 75.00,
                'total_seats': 400,
                'available_seats': 400,
                'genre': 'Hip Hop',
                'description': 'The hottest hip hop artists performing live',
                'created_at': datetime.now()
            },
            {
                'name': 'Country Music Festival',
                'artist': 'Nashville Stars',
                'venue': 'Outdoor Amphitheater',
                'date': (datetime.now() + timedelta(days=50)).strftime('%Y-%m-%d'),
                'time': '17:00',
                'ticket_price': 65.00,
                'total_seats': 600,
                'available_seats': 600,
                'genre': 'Country',
                'description': 'Authentic country music under the open sky',
                'created_at': datetime.now()
            }
        ]
        
        result = db.concerts.insert_many(sample_concerts)
        print(f"✅ Inserted {len(result.inserted_ids)} sample concerts")
        
        # Insert sample bookings
        print("\n🎟️  Creating sample bookings...")
        
        concerts = list(db.concerts.find())
        sample_customers = [
            {'name': 'John Doe', 'email': 'john.doe@example.com', 'phone': '555-0101'},
            {'name': 'Jane Smith', 'email': 'jane.smith@example.com', 'phone': '555-0102'},
            {'name': 'Bob Johnson', 'email': 'bob.johnson@example.com', 'phone': '555-0103'},
            {'name': 'Alice Williams', 'email': 'alice.williams@example.com', 'phone': '555-0104'},
            {'name': 'Charlie Brown', 'email': 'charlie.brown@example.com', 'phone': '555-0105'},
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
