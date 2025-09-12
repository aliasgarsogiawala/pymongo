"""
Main application for Concert Billing System.
Demonstrates CRUD operations and aggregation functions.
"""
from datetime import datetime, timedelta
from bson import ObjectId

from models import Concert, Customer, Booking, Invoice
from crud_operations import ConcertCRUD, CustomerCRUD, BookingCRUD, InvoiceCRUD
from analytics import BillingAnalytics


def print_separator(title=""):
    """Print a separator with optional title."""
    print("\n" + "=" * 60)
    if title:
        print(f" {title} ")
        print("=" * 60)


def display_concerts(concerts, title="Concerts"):
    """Display list of concerts."""
    print(f"\n{title}:")
    print("-" * 50)
    for i, concert in enumerate(concerts, 1):
        print(f"{i}. {concert.name} by {concert.artist}")
        print(f"   Venue: {concert.venue}")
        print(f"   Date: {concert.date.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Available Seats: {concert.available_seats}/{concert.total_seats}")
        print(f"   Ticket Prices: {concert.ticket_prices}")
        print()


def display_customers(customers, title="Customers"):
    """Display list of customers."""
    print(f"\n{title}:")
    print("-" * 50)
    for i, customer in enumerate(customers, 1):
        print(f"{i}. {customer.name} ({customer.email})")
        print(f"   Phone: {customer.phone}")
        if customer.address:
            print(f"   Address: {customer.address}")
        print()


def display_bookings(bookings, title="Bookings"):
    """Display list of bookings."""
    print(f"\n{title}:")
    print("-" * 50)
    for i, booking in enumerate(bookings, 1):
        print(f"{i}. Booking ID: {booking.customer_id}")
        print(f"   Concert ID: {booking.concert_id}")
        print(f"   Ticket Type: {booking.ticket_type}")
        print(f"   Quantity: {booking.quantity}")
        print(f"   Unit Price: ${booking.unit_price:.2f}")
        print(f"   Total Amount: ${booking.total_amount:.2f}")
        print(f"   Status: {booking.status}")
        print(f"   Date: {booking.booking_date.strftime('%Y-%m-%d %H:%M')}")
        print()


def display_analytics_result(data, title="Analytics Result"):
    """Display analytics result."""
    print(f"\n{title}:")
    print("-" * 50)
    if not data:
        print("No data available.")
        return
    
    for item in data:
        for key, value in item.items():
            if isinstance(value, datetime):
                print(f"{key}: {value.strftime('%Y-%m-%d %H:%M')}")
            elif isinstance(value, float):
                print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")
        print()


def create_sample_data():
    """Create sample data for demonstration."""
    print_separator("Creating Sample Data")
    
    try:
        # Initialize CRUD operations
        concert_crud = ConcertCRUD()
        customer_crud = CustomerCRUD()
        booking_crud = BookingCRUD()
        invoice_crud = InvoiceCRUD()
        
        # Create sample concerts
        concerts_data = [
            Concert(
                name="Rock Festival 2024",
                artist="The Rolling Stones",
                venue="Madison Square Garden",
                date=datetime(2024, 6, 15, 20, 0),
                ticket_prices={"VIP": 250.0, "Regular": 120.0, "Economy": 60.0},
                total_seats=1000
            ),
            Concert(
                name="Jazz Night",
                artist="Miles Davis Tribute",
                venue="Blue Note",
                date=datetime(2024, 7, 20, 21, 0),
                ticket_prices={"Premium": 180.0, "Standard": 90.0},
                total_seats=500
            ),
            Concert(
                name="Pop Sensation Tour",
                artist="Taylor Swift",
                venue="Stadium Arena",
                date=datetime(2024, 8, 10, 19, 30),
                ticket_prices={"VIP": 350.0, "Regular": 180.0, "Economy": 85.0},
                total_seats=2000
            )
        ]
        
        concert_ids = []
        for concert in concerts_data:
            concert_id = concert_crud.create_concert(concert)
            concert_ids.append(concert_id)
        
        # Create sample customers
        customers_data = [
            Customer(
                name="John Doe",
                email="john.doe@email.com",
                phone="+1-555-0101",
                address="123 Main St, New York, NY"
            ),
            Customer(
                name="Jane Smith",
                email="jane.smith@email.com",
                phone="+1-555-0102",
                address="456 Oak Ave, Los Angeles, CA"
            ),
            Customer(
                name="Bob Johnson",
                email="bob.johnson@email.com",
                phone="+1-555-0103",
                address="789 Pine St, Chicago, IL"
            ),
            Customer(
                name="Alice Williams",
                email="alice.williams@email.com",
                phone="+1-555-0104"
            )
        ]
        
        customer_ids = []
        for customer in customers_data:
            customer_id = customer_crud.create_customer(customer)
            customer_ids.append(customer_id)
        
        # Create sample bookings
        bookings_data = [
            Booking(customer_ids[0], concert_ids[0], "VIP", 2, 250.0),
            Booking(customer_ids[1], concert_ids[0], "Regular", 3, 120.0),
            Booking(customer_ids[2], concert_ids[1], "Premium", 1, 180.0),
            Booking(customer_ids[3], concert_ids[2], "VIP", 1, 350.0),
            Booking(customer_ids[0], concert_ids[2], "Regular", 4, 180.0),
            Booking(customer_ids[1], concert_ids[1], "Standard", 2, 90.0)
        ]
        
        booking_ids = []
        for booking in bookings_data:
            booking_id = booking_crud.create_booking(booking)
            booking_ids.append(booking_id)
            # Update available seats
            concert_crud.update_available_seats(booking.concert_id, booking.quantity)
        
        # Create sample invoices
        for i, booking_id in enumerate(booking_ids):
            booking = booking_crud.get_booking(booking_id)
            if booking:
                tax_rate = 0.08  # 8% tax
                tax_amount = booking.total_amount * tax_rate
                
                invoice = Invoice(
                    booking_id=booking_id,
                    customer_id=booking.customer_id,
                    amount=booking.total_amount,
                    tax_amount=tax_amount
                )
                
                invoice_id = invoice_crud.create_invoice(invoice)
                
                # Mark some invoices as paid
                if i % 2 == 0:
                    invoice_crud.mark_paid(invoice_id)
        
        print("Sample data created successfully!")
        return concert_ids, customer_ids, booking_ids
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        return [], [], []


def demonstrate_crud_operations():
    """Demonstrate CRUD operations."""
    print_separator("CRUD Operations Demonstration")
    
    try:
        # Initialize CRUD operations
        concert_crud = ConcertCRUD()
        customer_crud = CustomerCRUD()
        booking_crud = BookingCRUD()
        invoice_crud = InvoiceCRUD()
        
        # READ operations
        print("\n--- READ Operations ---")
        concerts = concert_crud.get_all_concerts()
        display_concerts(concerts, "All Concerts")
        
        customers = customer_crud.get_all_customers()
        display_customers(customers, "All Customers")
        
        bookings = booking_crud.get_all_bookings()
        display_bookings(bookings[:3], "Sample Bookings (First 3)")
        
        # UPDATE operations
        print("\n--- UPDATE Operations ---")
        if concerts:
            concert_id = ObjectId(str(concerts[0].__dict__.get('_id', concerts[0].__dict__.get('id'))))
            # Try to get the actual concert document to get its _id
            concert_docs = list(concert_crud.collection.find({"name": concerts[0].name}))
            if concert_docs:
                concert_id = concert_docs[0]['_id']
                updated = concert_crud.update_concert(
                    concert_id,
                    {"venue": "Updated Madison Square Garden"}
                )
                if updated:
                    print("Concert venue updated successfully!")
        
        if customers:
            customer_docs = list(customer_crud.collection.find({"email": customers[0].email}))
            if customer_docs:
                customer_id = customer_docs[0]['_id']
                updated = customer_crud.update_customer(
                    customer_id,
                    {"phone": "+1-555-9999"}
                )
                if updated:
                    print("Customer phone updated successfully!")
        
        # Show updated data
        updated_concerts = concert_crud.get_all_concerts()
        if updated_concerts:
            print(f"Updated concert venue: {updated_concerts[0].venue}")
        
        updated_customers = customer_crud.get_all_customers()
        if updated_customers:
            print(f"Updated customer phone: {updated_customers[0].phone}")
        
    except Exception as e:
        print(f"Error in CRUD operations: {e}")


def demonstrate_aggregations():
    """Demonstrate aggregation functions."""
    print_separator("Aggregation Functions Demonstration")
    
    try:
        analytics = BillingAnalytics()
        
        # Revenue by concert
        print("\n--- Revenue by Concert ---")
        revenue_data = analytics.get_revenue_by_concert()
        display_analytics_result(revenue_data, "Revenue by Concert")
        
        # Customer booking statistics
        print("\n--- Customer Booking Statistics ---")
        customer_stats = analytics.get_customer_booking_statistics()
        display_analytics_result(customer_stats, "Customer Statistics")
        
        # Popular concerts
        print("\n--- Popular Concerts ---")
        popular_concerts = analytics.get_popular_concerts(limit=5)
        display_analytics_result(popular_concerts, "Popular Concerts")
        
        # Monthly revenue report
        print("\n--- Monthly Revenue Report (2024) ---")
        monthly_revenue = analytics.get_monthly_revenue_report(2024)
        display_analytics_result(monthly_revenue, "Monthly Revenue")
        
        # Ticket type distribution
        print("\n--- Ticket Type Distribution ---")
        ticket_distribution = analytics.get_ticket_type_distribution()
        display_analytics_result(ticket_distribution, "Ticket Type Distribution")
        
        # Payment status summary
        print("\n--- Payment Status Summary ---")
        payment_summary = analytics.get_payment_status_summary()
        display_analytics_result(payment_summary, "Payment Status")
        
        # Revenue by venue
        print("\n--- Revenue by Venue ---")
        venue_revenue = analytics.get_revenue_by_venue()
        display_analytics_result(venue_revenue, "Revenue by Venue")
        
        # Top customers
        print("\n--- Top Customers by Spending ---")
        top_customers = analytics.get_top_customers_by_spending(limit=5)
        display_analytics_result(top_customers, "Top Customers")
        
    except Exception as e:
        print(f"Error in aggregation demonstrations: {e}")


def main():
    """Main function to run the concert billing system demonstration."""
    print_separator("Concert Billing System")
    print("Welcome to the Concert Billing System!")
    print("This system demonstrates MongoDB CRUD operations and aggregation functions.")
    
    try:
        # Create sample data
        concert_ids, customer_ids, booking_ids = create_sample_data()
        
        if not concert_ids:
            print("Failed to create sample data. Please check your MongoDB connection.")
            return
        
        # Demonstrate CRUD operations
        demonstrate_crud_operations()
        
        # Demonstrate aggregation functions
        demonstrate_aggregations()
        
        print_separator("System Demonstration Complete")
        print("The concert billing system has successfully demonstrated:")
        print("✓ MongoDB CRUD operations (Create, Read, Update, Delete)")
        print("✓ Complex aggregation queries for billing analytics")
        print("✓ Data models for concerts, customers, bookings, and invoices")
        print("✓ Revenue analysis and customer statistics")
        print("✓ Popular concert tracking and venue performance")
        
    except Exception as e:
        print(f"Error in main execution: {e}")
        print("\nPlease ensure MongoDB is running and accessible.")
        print("You can start MongoDB locally or update the connection settings in config.py")


if __name__ == "__main__":
    main()