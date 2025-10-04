"""
Seed script to populate MongoDB Atlas with sample concert billing data.
"""
from datetime import datetime, timedelta
from config import get_database
from models import Concert, Customer, Booking, Invoice
from crud_operations import ConcertCRUD, CustomerCRUD, BookingCRUD, InvoiceCRUD


def seed_data():
    """Seed the database with sample data."""
    print("🌱 Starting to seed MongoDB Atlas with sample data...")
    
    # Get database connection
    db = get_database()
    if not db:
        print("❌ Failed to connect to database. Exiting.")
        return
    
    # Initialize CRUD operations
    concert_crud = ConcertCRUD(db)
    customer_crud = CustomerCRUD(db)
    booking_crud = BookingCRUD(db)
    invoice_crud = InvoiceCRUD(db)
    
    try:
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("🧹 Clearing existing data...")
        db.concerts.delete_many({})
        db.customers.delete_many({})
        db.bookings.delete_many({})
        db.invoices.delete_many({})
        
        # Create sample concerts
        print("🎵 Creating sample concerts...")
        concerts_data = [
            {
                "name": "Rock Festival 2024",
                "artist": "The Rock Band",
                "venue": "Madison Square Garden",
                "date": datetime.now() + timedelta(days=30),
                "total_seats": 5000,
                "available_seats": 4500,
                "ticket_prices": {"VIP": 200, "Premium": 150, "Regular": 100}
            },
            {
                "name": "Jazz Night",
                "artist": "Miles Davis Tribute",
                "venue": "Blue Note",
                "date": datetime.now() + timedelta(days=45),
                "total_seats": 200,
                "available_seats": 180,
                "ticket_prices": {"VIP": 120, "Regular": 80}
            },
            {
                "name": "Pop Sensation Tour",
                "artist": "Taylor Swift",
                "venue": "Wembley Stadium",
                "date": datetime.now() + timedelta(days=60),
                "total_seats": 90000,
                "available_seats": 85000,
                "ticket_prices": {"VIP": 500, "Premium": 300, "Regular": 150}
            }
        ]
        
        created_concerts = []
        for concert_data in concerts_data:
            concert = Concert(**concert_data)
            concert_id = concert_crud.create_concert(concert)
            created_concerts.append(concert_id)
            print(f"   ✅ Created concert: {concert_data['name']}")
        
        # Create sample customers
        print("👥 Creating sample customers...")
        customers_data = [
            {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-0123",
                "address": "123 Main St, New York, NY 10001"
            },
            {
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "phone": "+1-555-0456",
                "address": "456 Oak Ave, Los Angeles, CA 90210"
            },
            {
                "name": "Bob Johnson",
                "email": "bob.johnson@example.com",
                "phone": "+1-555-0789",
                "address": "789 Pine St, Chicago, IL 60601"
            }
        ]
        
        created_customers = []
        for customer_data in customers_data:
            customer = Customer(**customer_data)
            customer_id = customer_crud.create_customer(customer)
            created_customers.append(customer_id)
            print(f"   ✅ Created customer: {customer_data['name']}")
        
        # Create sample bookings
        print("🎫 Creating sample bookings...")
        bookings_data = [
            {
                "customer_id": created_customers[0],
                "concert_id": created_concerts[0],
                "tickets": {"VIP": 2, "Regular": 1},
                "total_amount": 500.0,
                "booking_date": datetime.now() - timedelta(days=5),
                "status": "confirmed"
            },
            {
                "customer_id": created_customers[1],
                "concert_id": created_concerts[1],
                "tickets": {"Regular": 3},
                "total_amount": 240.0,
                "booking_date": datetime.now() - timedelta(days=3),
                "status": "confirmed"
            },
            {
                "customer_id": created_customers[2],
                "concert_id": created_concerts[2],
                "tickets": {"Premium": 2},
                "total_amount": 600.0,
                "booking_date": datetime.now() - timedelta(days=1),
                "status": "pending"
            }
        ]
        
        created_bookings = []
        for booking_data in bookings_data:
            booking = Booking(**booking_data)
            booking_id = booking_crud.create_booking(booking)
            created_bookings.append(booking_id)
            print(f"   ✅ Created booking for customer ID: {booking_data['customer_id']}")
        
        # Create sample invoices
        print("📄 Creating sample invoices...")
        invoices_data = [
            {
                "booking_id": created_bookings[0],
                "customer_id": created_customers[0],
                "amount": 500.0,
                "tax_amount": 50.0,
                "total_amount": 550.0,
                "issue_date": datetime.now() - timedelta(days=5),
                "due_date": datetime.now() + timedelta(days=25),
                "status": "paid",
                "payment_date": datetime.now() - timedelta(days=2)
            },
            {
                "booking_id": created_bookings[1],
                "customer_id": created_customers[1],
                "amount": 240.0,
                "tax_amount": 24.0,
                "total_amount": 264.0,
                "issue_date": datetime.now() - timedelta(days=3),
                "due_date": datetime.now() + timedelta(days=27),
                "status": "pending"
            },
            {
                "booking_id": created_bookings[2],
                "customer_id": created_customers[2],
                "amount": 600.0,
                "tax_amount": 60.0,
                "total_amount": 660.0,
                "issue_date": datetime.now() - timedelta(days=1),
                "due_date": datetime.now() + timedelta(days=29),
                "status": "overdue"
            }
        ]
        
        for invoice_data in invoices_data:
            invoice = Invoice(**invoice_data)
            invoice_id = invoice_crud.create_invoice(invoice)
            print(f"   ✅ Created invoice for booking ID: {invoice_data['booking_id']}")
        
        print("\n🎉 Sample data seeding completed successfully!")
        print(f"📊 Created:")
        print(f"   - {len(created_concerts)} concerts")
        print(f"   - {len(created_customers)} customers") 
        print(f"   - {len(created_bookings)} bookings")
        print(f"   - {len(invoices_data)} invoices")
        
    except Exception as e:
        print(f"❌ Error seeding data: {str(e)}")


if __name__ == "__main__":
    seed_data()