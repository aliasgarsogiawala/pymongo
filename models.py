"""
Data models for the concert billing system.
"""
from datetime import datetime
from typing import Dict, List, Optional
from bson import ObjectId

class Concert:
    """Concert model with event details and pricing."""
    
    def __init__(self, name: str, artist: str, venue: str, date: datetime, 
                 ticket_prices: Dict[str, float], total_seats: int):
        self.name = name
        self.artist = artist
        self.venue = venue
        self.date = date
        self.ticket_prices = ticket_prices  # e.g., {"VIP": 150.0, "Regular": 75.0, "Economy": 35.0}
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert Concert object to dictionary for MongoDB storage."""
        return {
            'name': self.name,
            'artist': self.artist,
            'venue': self.venue,
            'date': self.date,
            'ticket_prices': self.ticket_prices,
            'total_seats': self.total_seats,
            'available_seats': self.available_seats,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Concert':
        """Create Concert object from dictionary."""
        concert = cls(
            name=data['name'],
            artist=data['artist'],
            venue=data['venue'],
            date=data['date'],
            ticket_prices=data['ticket_prices'],
            total_seats=data['total_seats']
        )
        concert.available_seats = data.get('available_seats', data['total_seats'])
        concert.created_at = data.get('created_at', datetime.now())
        return concert


class Customer:
    """Customer model with personal information."""
    
    def __init__(self, name: str, email: str, phone: str, address: Optional[str] = None):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert Customer object to dictionary for MongoDB storage."""
        return {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Customer':
        """Create Customer object from dictionary."""
        customer = cls(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            address=data.get('address')
        )
        customer.created_at = data.get('created_at', datetime.now())
        return customer


class Booking:
    """Booking model linking customers to concerts with tickets."""
    
    def __init__(self, customer_id: ObjectId, concert_id: ObjectId, 
                 ticket_type: str, quantity: int, unit_price: float):
        self.customer_id = customer_id
        self.concert_id = concert_id
        self.ticket_type = ticket_type
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_amount = quantity * unit_price
        self.booking_date = datetime.now()
        self.status = "confirmed"  # confirmed, cancelled, refunded
    
    def to_dict(self) -> Dict:
        """Convert Booking object to dictionary for MongoDB storage."""
        return {
            'customer_id': self.customer_id,
            'concert_id': self.concert_id,
            'ticket_type': self.ticket_type,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_amount': self.total_amount,
            'booking_date': self.booking_date,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Booking':
        """Create Booking object from dictionary."""
        booking = cls(
            customer_id=data['customer_id'],
            concert_id=data['concert_id'],
            ticket_type=data['ticket_type'],
            quantity=data['quantity'],
            unit_price=data['unit_price']
        )
        booking.total_amount = data.get('total_amount', booking.total_amount)
        booking.booking_date = data.get('booking_date', datetime.now())
        booking.status = data.get('status', 'confirmed')
        return booking


class Invoice:
    """Invoice model for billing information."""
    
    def __init__(self, booking_id: ObjectId, customer_id: ObjectId, 
                 amount: float, tax_amount: float = 0.0):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.amount = amount
        self.tax_amount = tax_amount
        self.total_amount = amount + tax_amount
        self.issue_date = datetime.now()
        self.payment_status = "pending"  # pending, paid, overdue, cancelled
        self.payment_date = None
        self.invoice_number = self._generate_invoice_number()
    
    def _generate_invoice_number(self) -> str:
        """Generate unique invoice number."""
        timestamp = int(datetime.now().timestamp())
        return f"INV-{timestamp}"
    
    def to_dict(self) -> Dict:
        """Convert Invoice object to dictionary for MongoDB storage."""
        return {
            'booking_id': self.booking_id,
            'customer_id': self.customer_id,
            'amount': self.amount,
            'tax_amount': self.tax_amount,
            'total_amount': self.total_amount,
            'issue_date': self.issue_date,
            'payment_status': self.payment_status,
            'payment_date': self.payment_date,
            'invoice_number': self.invoice_number
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Invoice':
        """Create Invoice object from dictionary."""
        invoice = cls(
            booking_id=data['booking_id'],
            customer_id=data['customer_id'],
            amount=data['amount'],
            tax_amount=data.get('tax_amount', 0.0)
        )
        invoice.total_amount = data.get('total_amount', invoice.total_amount)
        invoice.issue_date = data.get('issue_date', datetime.now())
        invoice.payment_status = data.get('payment_status', 'pending')
        invoice.payment_date = data.get('payment_date')
        invoice.invoice_number = data.get('invoice_number', invoice.invoice_number)
        return invoice