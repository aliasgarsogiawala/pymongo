# Concert Billing System

A comprehensive concert billing system built with Python and MongoDB that demonstrates CRUD operations and aggregation functions for managing concerts, customers, bookings, and invoices.

## Features

### Core Functionality
- **Concert Management**: Create, read, update, and delete concert events
- **Customer Management**: Handle customer information and profiles
- **Booking System**: Process ticket bookings with different types and pricing
- **Invoice Generation**: Automatic billing with tax calculations and payment tracking

### MongoDB Operations
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality for all entities
- **Advanced Aggregations**: Complex analytical queries for business insights
- **Data Relationships**: Proper linking between concerts, customers, bookings, and invoices

### Analytics & Reporting
- Revenue analysis by concert, venue, and time period
- Customer behavior and spending statistics
- Popular concert tracking and ticket distribution
- Payment status monitoring and financial reporting

## Project Structure

```
pymongo/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── config.py                # Database configuration
├── models.py                # Data models (Concert, Customer, Booking, Invoice)
├── crud_operations.py       # CRUD operations for all models
├── analytics.py             # MongoDB aggregation functions
├── main.py                  # Main application demonstrating functionality
└── test_billing_system.py   # Basic test suite
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- MongoDB server (local or remote)

### Installation Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure MongoDB Connection**
   - Update `config.py` if using non-default MongoDB settings
   - Default configuration connects to `localhost:27017`
   - Database name: `concert_billing`

3. **Start MongoDB Service**
   ```bash
   # On Ubuntu/Debian
   sudo systemctl start mongod
   
   # On macOS with Homebrew
   brew services start mongodb-community
   
   # Using Docker
   docker run -d -p 27017:27017 --name mongodb mongo
   ```

## Usage

### Running the Main Application

```bash
python main.py
```

This will:
- Create sample data (concerts, customers, bookings, invoices)
- Demonstrate all CRUD operations
- Execute various aggregation queries
- Display comprehensive analytics reports

### Running Tests

```bash
python test_billing_system.py
```

### Using Individual Components

```python
from crud_operations import ConcertCRUD, CustomerCRUD
from models import Concert, Customer
from analytics import BillingAnalytics
from datetime import datetime

# Create a new concert
concert_crud = ConcertCRUD()
concert = Concert(
    name="Rock Festival 2024",
    artist="The Rolling Stones", 
    venue="Madison Square Garden",
    date=datetime(2024, 6, 15, 20, 0),
    ticket_prices={"VIP": 250.0, "Regular": 120.0},
    total_seats=1000
)
concert_id = concert_crud.create_concert(concert)

# Get analytics
analytics = BillingAnalytics()
revenue_data = analytics.get_revenue_by_concert()
```

## Data Models

### Concert
- Event details (name, artist, venue, date)
- Ticket pricing tiers
- Seat availability tracking

### Customer  
- Personal information (name, email, phone, address)
- Registration timestamps

### Booking
- Links customers to concerts
- Ticket type and quantity
- Pricing and total calculations
- Status tracking (confirmed, cancelled, refunded)

### Invoice
- Billing information for bookings
- Tax calculations
- Payment status tracking
- Unique invoice numbering

## MongoDB Aggregation Queries

The system includes sophisticated aggregation pipelines for:

- **Revenue Analysis**: Total revenue by concert, venue, and time periods
- **Customer Insights**: Booking patterns and spending behavior
- **Performance Metrics**: Concert popularity and ticket distribution
- **Financial Reporting**: Payment status summaries and revenue forecasting

## Configuration

### Environment Variables
- `MONGODB_HOST`: MongoDB server hostname (default: localhost)
- `MONGODB_PORT`: MongoDB server port (default: 27017)  
- `DATABASE_NAME`: Database name (default: concert_billing)

### Database Collections
- `concerts`: Concert event information
- `customers`: Customer profiles
- `bookings`: Ticket booking records
- `invoices`: Billing and payment data

## Error Handling

The system includes comprehensive error handling for:
- Database connection failures
- Invalid data inputs
- Document not found scenarios
- MongoDB operation errors

## Sample Output

When running `main.py`, you'll see:

1. **Sample Data Creation**: Concerts, customers, and bookings
2. **CRUD Operations**: Create, read, update, delete demonstrations
3. **Analytics Reports**: Revenue analysis, customer statistics, popular concerts
4. **Payment Tracking**: Invoice generation and payment processing

## Contributing

This is an educational project demonstrating MongoDB operations with Python. Feel free to extend it with additional features like:

- Web interface using Flask/Django
- Advanced booking validations
- Email notifications
- Reporting dashboard
- Multi-currency support

## License

This project is for educational purposes and demonstrates MongoDB CRUD operations and aggregation functions in a practical billing system context.