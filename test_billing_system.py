"""
Basic tests for the concert billing system.
Note: These tests require a running MongoDB instance.
"""
import unittest
from datetime import datetime
from bson import ObjectId

from models import Concert, Customer, Booking, Invoice
from crud_operations import ConcertCRUD, CustomerCRUD, BookingCRUD, InvoiceCRUD


class TestConcertBillingSystem(unittest.TestCase):
    """Test cases for the concert billing system."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            self.concert_crud = ConcertCRUD()
            self.customer_crud = CustomerCRUD()
            self.booking_crud = BookingCRUD()
            self.invoice_crud = InvoiceCRUD()
            
            # Test data
            self.test_concert = Concert(
                name="Test Concert",
                artist="Test Artist",
                venue="Test Venue",
                date=datetime(2024, 12, 31, 20, 0),
                ticket_prices={"VIP": 100.0, "Regular": 50.0},
                total_seats=100
            )
            
            self.test_customer = Customer(
                name="Test Customer",
                email="test@example.com",
                phone="+1-555-0000"
            )
            
        except Exception as e:
            self.skipTest(f"Cannot connect to MongoDB: {e}")
    
    def test_concert_crud(self):
        """Test concert CRUD operations."""
        # CREATE
        concert_id = self.concert_crud.create_concert(self.test_concert)
        self.assertIsInstance(concert_id, ObjectId)
        
        # READ
        retrieved_concert = self.concert_crud.get_concert(concert_id)
        self.assertIsNotNone(retrieved_concert)
        self.assertEqual(retrieved_concert.name, "Test Concert")
        self.assertEqual(retrieved_concert.artist, "Test Artist")
        
        # UPDATE
        updated = self.concert_crud.update_concert(
            concert_id,
            {"venue": "Updated Test Venue"}
        )
        self.assertTrue(updated)
        
        updated_concert = self.concert_crud.get_concert(concert_id)
        self.assertEqual(updated_concert.venue, "Updated Test Venue")
        
        # DELETE
        deleted = self.concert_crud.delete_concert(concert_id)
        self.assertTrue(deleted)
        
        # Verify deletion
        deleted_concert = self.concert_crud.get_concert(concert_id)
        self.assertIsNone(deleted_concert)
    
    def test_customer_crud(self):
        """Test customer CRUD operations."""
        # CREATE
        customer_id = self.customer_crud.create_customer(self.test_customer)
        self.assertIsInstance(customer_id, ObjectId)
        
        # READ
        retrieved_customer = self.customer_crud.get_customer(customer_id)
        self.assertIsNotNone(retrieved_customer)
        self.assertEqual(retrieved_customer.name, "Test Customer")
        self.assertEqual(retrieved_customer.email, "test@example.com")
        
        # READ by email
        customer_by_email = self.customer_crud.get_customer_by_email("test@example.com")
        self.assertIsNotNone(customer_by_email)
        self.assertEqual(customer_by_email.name, "Test Customer")
        
        # UPDATE
        updated = self.customer_crud.update_customer(
            customer_id,
            {"phone": "+1-555-1111"}
        )
        self.assertTrue(updated)
        
        # DELETE
        deleted = self.customer_crud.delete_customer(customer_id)
        self.assertTrue(deleted)
    
    def test_booking_workflow(self):
        """Test complete booking workflow."""
        # First create concert and customer
        concert_id = self.concert_crud.create_concert(self.test_concert)
        customer_id = self.customer_crud.create_customer(self.test_customer)
        
        try:
            # Create booking
            test_booking = Booking(
                customer_id=customer_id,
                concert_id=concert_id,
                ticket_type="Regular",
                quantity=2,
                unit_price=50.0
            )
            
            booking_id = self.booking_crud.create_booking(test_booking)
            self.assertIsInstance(booking_id, ObjectId)
            
            # Verify booking
            retrieved_booking = self.booking_crud.get_booking(booking_id)
            self.assertIsNotNone(retrieved_booking)
            self.assertEqual(retrieved_booking.quantity, 2)
            self.assertEqual(retrieved_booking.total_amount, 100.0)
            
            # Create invoice for booking
            test_invoice = Invoice(
                booking_id=booking_id,
                customer_id=customer_id,
                amount=100.0,
                tax_amount=8.0
            )
            
            invoice_id = self.invoice_crud.create_invoice(test_invoice)
            self.assertIsInstance(invoice_id, ObjectId)
            
            # Verify invoice
            retrieved_invoice = self.invoice_crud.get_invoice(invoice_id)
            self.assertIsNotNone(retrieved_invoice)
            self.assertEqual(retrieved_invoice.total_amount, 108.0)
            self.assertEqual(retrieved_invoice.payment_status, "pending")
            
            # Mark invoice as paid
            paid = self.invoice_crud.mark_paid(invoice_id)
            self.assertTrue(paid)
            
            # Verify payment status
            paid_invoice = self.invoice_crud.get_invoice(invoice_id)
            self.assertEqual(paid_invoice.payment_status, "paid")
            self.assertIsNotNone(paid_invoice.payment_date)
            
        finally:
            # Cleanup
            self.booking_crud.delete_booking(booking_id)
            self.invoice_crud.delete_invoice(invoice_id)
            self.concert_crud.delete_concert(concert_id)
            self.customer_crud.delete_customer(customer_id)
    
    def test_model_validation(self):
        """Test model data validation."""
        # Test Concert model
        concert_dict = self.test_concert.to_dict()
        self.assertIn('name', concert_dict)
        self.assertIn('ticket_prices', concert_dict)
        self.assertEqual(concert_dict['total_seats'], 100)
        
        recreated_concert = Concert.from_dict(concert_dict)
        self.assertEqual(recreated_concert.name, self.test_concert.name)
        self.assertEqual(recreated_concert.venue, self.test_concert.venue)
        
        # Test Customer model
        customer_dict = self.test_customer.to_dict()
        self.assertIn('name', customer_dict)
        self.assertIn('email', customer_dict)
        
        recreated_customer = Customer.from_dict(customer_dict)
        self.assertEqual(recreated_customer.email, self.test_customer.email)


def run_tests():
    """Run all tests."""
    print("Running Concert Billing System Tests...")
    print("Note: These tests require a running MongoDB instance.")
    print("-" * 50)
    
    unittest.main(verbosity=2, exit=False)


if __name__ == "__main__":
    run_tests()