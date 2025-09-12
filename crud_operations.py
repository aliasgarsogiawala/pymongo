"""
CRUD operations for the concert billing system.
"""
from typing import Dict, List, Optional
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from datetime import datetime

from config import get_database, CONCERTS_COLLECTION, CUSTOMERS_COLLECTION, BOOKINGS_COLLECTION, INVOICES_COLLECTION
from models import Concert, Customer, Booking, Invoice


class ConcertCRUD:
    """CRUD operations for concerts."""
    
    def __init__(self):
        self.db = get_database()
        if self.db is None:
            raise Exception("Failed to connect to database")
        self.collection: Collection = self.db[CONCERTS_COLLECTION]
    
    def create_concert(self, concert: Concert) -> ObjectId:
        """Create a new concert."""
        try:
            result = self.collection.insert_one(concert.to_dict())
            print(f"Concert created with ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            print(f"Error creating concert: {e}")
            raise
    
    def get_concert(self, concert_id: ObjectId) -> Optional[Concert]:
        """Get a concert by ID."""
        try:
            doc = self.collection.find_one({"_id": concert_id})
            if doc:
                return Concert.from_dict(doc)
            return None
        except PyMongoError as e:
            print(f"Error getting concert: {e}")
            return None
    
    def get_all_concerts(self) -> List[Concert]:
        """Get all concerts."""
        try:
            docs = self.collection.find()
            return [Concert.from_dict(doc) for doc in docs]
        except PyMongoError as e:
            print(f"Error getting concerts: {e}")
            return []
    
    def update_concert(self, concert_id: ObjectId, update_data: Dict) -> bool:
        """Update a concert."""
        try:
            result = self.collection.update_one(
                {"_id": concert_id},
                {"$set": update_data}
            )
            if result.modified_count > 0:
                print(f"Concert {concert_id} updated successfully")
                return True
            else:
                print(f"Concert {concert_id} not found or no changes made")
                return False
        except PyMongoError as e:
            print(f"Error updating concert: {e}")
            return False
    
    def delete_concert(self, concert_id: ObjectId) -> bool:
        """Delete a concert."""
        try:
            result = self.collection.delete_one({"_id": concert_id})
            if result.deleted_count > 0:
                print(f"Concert {concert_id} deleted successfully")
                return True
            else:
                print(f"Concert {concert_id} not found")
                return False
        except PyMongoError as e:
            print(f"Error deleting concert: {e}")
            return False
    
    def update_available_seats(self, concert_id: ObjectId, seats_booked: int) -> bool:
        """Update available seats for a concert."""
        try:
            result = self.collection.update_one(
                {"_id": concert_id},
                {"$inc": {"available_seats": -seats_booked}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            print(f"Error updating seats: {e}")
            return False


class CustomerCRUD:
    """CRUD operations for customers."""
    
    def __init__(self):
        self.db = get_database()
        if self.db is None:
            raise Exception("Failed to connect to database")
        self.collection: Collection = self.db[CUSTOMERS_COLLECTION]
    
    def create_customer(self, customer: Customer) -> ObjectId:
        """Create a new customer."""
        try:
            result = self.collection.insert_one(customer.to_dict())
            print(f"Customer created with ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            print(f"Error creating customer: {e}")
            raise
    
    def get_customer(self, customer_id: ObjectId) -> Optional[Customer]:
        """Get a customer by ID."""
        try:
            doc = self.collection.find_one({"_id": customer_id})
            if doc:
                return Customer.from_dict(doc)
            return None
        except PyMongoError as e:
            print(f"Error getting customer: {e}")
            return None
    
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Get a customer by email."""
        try:
            doc = self.collection.find_one({"email": email})
            if doc:
                return Customer.from_dict(doc)
            return None
        except PyMongoError as e:
            print(f"Error getting customer by email: {e}")
            return None
    
    def get_all_customers(self) -> List[Customer]:
        """Get all customers."""
        try:
            docs = self.collection.find()
            return [Customer.from_dict(doc) for doc in docs]
        except PyMongoError as e:
            print(f"Error getting customers: {e}")
            return []
    
    def update_customer(self, customer_id: ObjectId, update_data: Dict) -> bool:
        """Update a customer."""
        try:
            result = self.collection.update_one(
                {"_id": customer_id},
                {"$set": update_data}
            )
            if result.modified_count > 0:
                print(f"Customer {customer_id} updated successfully")
                return True
            else:
                print(f"Customer {customer_id} not found or no changes made")
                return False
        except PyMongoError as e:
            print(f"Error updating customer: {e}")
            return False
    
    def delete_customer(self, customer_id: ObjectId) -> bool:
        """Delete a customer."""
        try:
            result = self.collection.delete_one({"_id": customer_id})
            if result.deleted_count > 0:
                print(f"Customer {customer_id} deleted successfully")
                return True
            else:
                print(f"Customer {customer_id} not found")
                return False
        except PyMongoError as e:
            print(f"Error deleting customer: {e}")
            return False


class BookingCRUD:
    """CRUD operations for bookings."""
    
    def __init__(self):
        self.db = get_database()
        if self.db is None:
            raise Exception("Failed to connect to database")
        self.collection: Collection = self.db[BOOKINGS_COLLECTION]
    
    def create_booking(self, booking: Booking) -> ObjectId:
        """Create a new booking."""
        try:
            result = self.collection.insert_one(booking.to_dict())
            print(f"Booking created with ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            print(f"Error creating booking: {e}")
            raise
    
    def get_booking(self, booking_id: ObjectId) -> Optional[Booking]:
        """Get a booking by ID."""
        try:
            doc = self.collection.find_one({"_id": booking_id})
            if doc:
                return Booking.from_dict(doc)
            return None
        except PyMongoError as e:
            print(f"Error getting booking: {e}")
            return None
    
    def get_bookings_by_customer(self, customer_id: ObjectId) -> List[Booking]:
        """Get all bookings for a customer."""
        try:
            docs = self.collection.find({"customer_id": customer_id})
            return [Booking.from_dict(doc) for doc in docs]
        except PyMongoError as e:
            print(f"Error getting customer bookings: {e}")
            return []
    
    def get_bookings_by_concert(self, concert_id: ObjectId) -> List[Booking]:
        """Get all bookings for a concert."""
        try:
            docs = self.collection.find({"concert_id": concert_id})
            return [Booking.from_dict(doc) for doc in docs]
        except PyMongoError as e:
            print(f"Error getting concert bookings: {e}")
            return []
    
    def get_all_bookings(self) -> List[Booking]:
        """Get all bookings."""
        try:
            docs = self.collection.find()
            return [Booking.from_dict(doc) for doc in docs]
        except PyMongoError as e:
            print(f"Error getting bookings: {e}")
            return []
    
    def update_booking(self, booking_id: ObjectId, update_data: Dict) -> bool:
        """Update a booking."""
        try:
            result = self.collection.update_one(
                {"_id": booking_id},
                {"$set": update_data}
            )
            if result.modified_count > 0:
                print(f"Booking {booking_id} updated successfully")
                return True
            else:
                print(f"Booking {booking_id} not found or no changes made")
                return False
        except PyMongoError as e:
            print(f"Error updating booking: {e}")
            return False
    
    def cancel_booking(self, booking_id: ObjectId) -> bool:
        """Cancel a booking."""
        return self.update_booking(booking_id, {"status": "cancelled"})
    
    def delete_booking(self, booking_id: ObjectId) -> bool:
        """Delete a booking."""
        try:
            result = self.collection.delete_one({"_id": booking_id})
            if result.deleted_count > 0:
                print(f"Booking {booking_id} deleted successfully")
                return True
            else:
                print(f"Booking {booking_id} not found")
                return False
        except PyMongoError as e:
            print(f"Error deleting booking: {e}")
            return False


class InvoiceCRUD:
    """CRUD operations for invoices."""
    
    def __init__(self):
        self.db = get_database()
        if self.db is None:
            raise Exception("Failed to connect to database")
        self.collection: Collection = self.db[INVOICES_COLLECTION]
    
    def create_invoice(self, invoice: Invoice) -> ObjectId:
        """Create a new invoice."""
        try:
            result = self.collection.insert_one(invoice.to_dict())
            print(f"Invoice created with ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            print(f"Error creating invoice: {e}")
            raise
    
    def get_invoice(self, invoice_id: ObjectId) -> Optional[Invoice]:
        """Get an invoice by ID."""
        try:
            doc = self.collection.find_one({"_id": invoice_id})
            if doc:
                return Invoice.from_dict(doc)
            return None
        except PyMongoError as e:
            print(f"Error getting invoice: {e}")
            return None
    
    def get_invoice_by_booking(self, booking_id: ObjectId) -> Optional[Invoice]:
        """Get an invoice by booking ID."""
        try:
            doc = self.collection.find_one({"booking_id": booking_id})
            if doc:
                return Invoice.from_dict(doc)
            return None
        except PyMongoError as e:
            print(f"Error getting invoice by booking: {e}")
            return None
    
    def get_invoices_by_customer(self, customer_id: ObjectId) -> List[Invoice]:
        """Get all invoices for a customer."""
        try:
            docs = self.collection.find({"customer_id": customer_id})
            return [Invoice.from_dict(doc) for doc in docs]
        except PyMongoError as e:
            print(f"Error getting customer invoices: {e}")
            return []
    
    def get_all_invoices(self) -> List[Invoice]:
        """Get all invoices."""
        try:
            docs = self.collection.find()
            return [Invoice.from_dict(doc) for doc in docs]
        except PyMongoError as e:
            print(f"Error getting invoices: {e}")
            return []
    
    def update_invoice(self, invoice_id: ObjectId, update_data: Dict) -> bool:
        """Update an invoice."""
        try:
            result = self.collection.update_one(
                {"_id": invoice_id},
                {"$set": update_data}
            )
            if result.modified_count > 0:
                print(f"Invoice {invoice_id} updated successfully")
                return True
            else:
                print(f"Invoice {invoice_id} not found or no changes made")
                return False
        except PyMongoError as e:
            print(f"Error updating invoice: {e}")
            return False
    
    def mark_paid(self, invoice_id: ObjectId, payment_date: datetime = None) -> bool:
        """Mark an invoice as paid."""
        if payment_date is None:
            payment_date = datetime.now()
        
        return self.update_invoice(invoice_id, {
            "payment_status": "paid",
            "payment_date": payment_date
        })
    
    def delete_invoice(self, invoice_id: ObjectId) -> bool:
        """Delete an invoice."""
        try:
            result = self.collection.delete_one({"_id": invoice_id})
            if result.deleted_count > 0:
                print(f"Invoice {invoice_id} deleted successfully")
                return True
            else:
                print(f"Invoice {invoice_id} not found")
                return False
        except PyMongoError as e:
            print(f"Error deleting invoice: {e}")
            return False