"""
MongoDB aggregation functions for concert billing system analytics.
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from config import get_database, CONCERTS_COLLECTION, CUSTOMERS_COLLECTION, BOOKINGS_COLLECTION, INVOICES_COLLECTION


class BillingAnalytics:
    """Aggregation functions for billing analytics and reporting."""
    
    def __init__(self):
        self.db = get_database()
        if self.db is None:
            raise Exception("Failed to connect to database")
        
        self.concerts_collection: Collection = self.db[CONCERTS_COLLECTION]
        self.customers_collection: Collection = self.db[CUSTOMERS_COLLECTION]
        self.bookings_collection: Collection = self.db[BOOKINGS_COLLECTION]
        self.invoices_collection: Collection = self.db[INVOICES_COLLECTION]
    
    def get_revenue_by_concert(self) -> List[Dict]:
        """
        Aggregate total revenue by concert.
        Returns list of concerts with their total revenue.
        """
        try:
            pipeline = [
                {
                    "$lookup": {
                        "from": BOOKINGS_COLLECTION,
                        "localField": "_id",
                        "foreignField": "concert_id",
                        "as": "bookings"
                    }
                },
                {
                    "$unwind": {
                        "path": "$bookings",
                        "preserveNullAndEmptyArrays": True
                    }
                },
                {
                    "$group": {
                        "_id": "$_id",
                        "concert_name": {"$first": "$name"},
                        "artist": {"$first": "$artist"},
                        "venue": {"$first": "$venue"},
                        "date": {"$first": "$date"},
                        "total_revenue": {"$sum": "$bookings.total_amount"},
                        "tickets_sold": {"$sum": "$bookings.quantity"},
                        "total_seats": {"$first": "$total_seats"}
                    }
                },
                {
                    "$addFields": {
                        "occupancy_rate": {
                            "$multiply": [
                                {"$divide": ["$tickets_sold", "$total_seats"]},
                                100
                            ]
                        }
                    }
                },
                {
                    "$sort": {"total_revenue": -1}
                }
            ]
            
            result = list(self.concerts_collection.aggregate(pipeline))
            return result
            
        except PyMongoError as e:
            print(f"Error in revenue by concert aggregation: {e}")
            return []
    
    def get_customer_booking_statistics(self) -> List[Dict]:
        """
        Aggregate customer booking statistics.
        Returns customer info with total bookings and spending.
        """
        try:
            pipeline = [
                {
                    "$lookup": {
                        "from": BOOKINGS_COLLECTION,
                        "localField": "_id",
                        "foreignField": "customer_id",
                        "as": "bookings"
                    }
                },
                {
                    "$addFields": {
                        "total_bookings": {"$size": "$bookings"},
                        "total_spent": {"$sum": "$bookings.total_amount"},
                        "avg_booking_value": {"$avg": "$bookings.total_amount"}
                    }
                },
                {
                    "$match": {
                        "total_bookings": {"$gt": 0}
                    }
                },
                {
                    "$project": {
                        "name": 1,
                        "email": 1,
                        "phone": 1,
                        "total_bookings": 1,
                        "total_spent": 1,
                        "avg_booking_value": {"$round": ["$avg_booking_value", 2]}
                    }
                },
                {
                    "$sort": {"total_spent": -1}
                }
            ]
            
            result = list(self.customers_collection.aggregate(pipeline))
            return result
            
        except PyMongoError as e:
            print(f"Error in customer statistics aggregation: {e}")
            return []
    
    def get_popular_concerts(self, limit: int = 10) -> List[Dict]:
        """
        Get most popular concerts by ticket sales.
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$concert_id",
                        "total_tickets_sold": {"$sum": "$quantity"},
                        "total_revenue": {"$sum": "$total_amount"},
                        "unique_customers": {"$addToSet": "$customer_id"}
                    }
                },
                {
                    "$lookup": {
                        "from": CONCERTS_COLLECTION,
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "concert_info"
                    }
                },
                {
                    "$unwind": "$concert_info"
                },
                {
                    "$addFields": {
                        "unique_customers_count": {"$size": "$unique_customers"}
                    }
                },
                {
                    "$project": {
                        "concert_name": "$concert_info.name",
                        "artist": "$concert_info.artist",
                        "venue": "$concert_info.venue",
                        "date": "$concert_info.date",
                        "total_tickets_sold": 1,
                        "total_revenue": 1,
                        "unique_customers_count": 1
                    }
                },
                {
                    "$sort": {"total_tickets_sold": -1}
                },
                {
                    "$limit": limit
                }
            ]
            
            result = list(self.bookings_collection.aggregate(pipeline))
            return result
            
        except PyMongoError as e:
            print(f"Error in popular concerts aggregation: {e}")
            return []
    
    def get_monthly_revenue_report(self, year: int = None) -> List[Dict]:
        """
        Get monthly revenue report for a specific year (default: current year).
        """
        if year is None:
            year = datetime.now().year
        
        try:
            pipeline = [
                {
                    "$match": {
                        "booking_date": {
                            "$gte": datetime(year, 1, 1),
                            "$lt": datetime(year + 1, 1, 1)
                        }
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "year": {"$year": "$booking_date"},
                            "month": {"$month": "$booking_date"}
                        },
                        "total_revenue": {"$sum": "$total_amount"},
                        "total_bookings": {"$sum": 1},
                        "total_tickets": {"$sum": "$quantity"},
                        "avg_booking_value": {"$avg": "$total_amount"}
                    }
                },
                {
                    "$addFields": {
                        "month_name": {
                            "$arrayElemAt": [
                                ["", "January", "February", "March", "April", "May", "June",
                                 "July", "August", "September", "October", "November", "December"],
                                "$_id.month"
                            ]
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "year": "$_id.year",
                        "month": "$_id.month",
                        "month_name": 1,
                        "total_revenue": 1,
                        "total_bookings": 1,
                        "total_tickets": 1,
                        "avg_booking_value": {"$round": ["$avg_booking_value", 2]}
                    }
                },
                {
                    "$sort": {"year": 1, "month": 1}
                }
            ]
            
            result = list(self.bookings_collection.aggregate(pipeline))
            return result
            
        except PyMongoError as e:
            print(f"Error in monthly revenue report aggregation: {e}")
            return []
    
    def get_ticket_type_distribution(self) -> List[Dict]:
        """
        Get distribution of ticket types sold.
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$ticket_type",
                        "quantity_sold": {"$sum": "$quantity"},
                        "total_revenue": {"$sum": "$total_amount"},
                        "avg_price": {"$avg": "$unit_price"},
                        "booking_count": {"$sum": 1}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "ticket_type": "$_id",
                        "quantity_sold": 1,
                        "total_revenue": 1,
                        "avg_price": {"$round": ["$avg_price", 2]},
                        "booking_count": 1
                    }
                },
                {
                    "$sort": {"total_revenue": -1}
                }
            ]
            
            result = list(self.bookings_collection.aggregate(pipeline))
            return result
            
        except PyMongoError as e:
            print(f"Error in ticket type distribution aggregation: {e}")
            return []
    
    def get_payment_status_summary(self) -> List[Dict]:
        """
        Get summary of payment statuses from invoices.
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$payment_status",
                        "count": {"$sum": 1},
                        "total_amount": {"$sum": "$total_amount"},
                        "avg_amount": {"$avg": "$total_amount"}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "payment_status": "$_id",
                        "count": 1,
                        "total_amount": 1,
                        "avg_amount": {"$round": ["$avg_amount", 2]}
                    }
                },
                {
                    "$sort": {"total_amount": -1}
                }
            ]
            
            result = list(self.invoices_collection.aggregate(pipeline))
            return result
            
        except PyMongoError as e:
            print(f"Error in payment status summary aggregation: {e}")
            return []
    
    def get_revenue_by_venue(self) -> List[Dict]:
        """
        Get total revenue by venue.
        """
        try:
            pipeline = [
                {
                    "$lookup": {
                        "from": BOOKINGS_COLLECTION,
                        "localField": "_id",
                        "foreignField": "concert_id",
                        "as": "bookings"
                    }
                },
                {
                    "$unwind": {
                        "path": "$bookings",
                        "preserveNullAndEmptyArrays": True
                    }
                },
                {
                    "$group": {
                        "_id": "$venue",
                        "total_revenue": {"$sum": "$bookings.total_amount"},
                        "total_concerts": {"$addToSet": "$_id"},
                        "total_tickets_sold": {"$sum": "$bookings.quantity"}
                    }
                },
                {
                    "$addFields": {
                        "total_concerts_count": {"$size": "$total_concerts"}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "venue": "$_id",
                        "total_revenue": 1,
                        "total_concerts_count": 1,
                        "total_tickets_sold": 1,
                        "avg_revenue_per_concert": {
                            "$divide": ["$total_revenue", "$total_concerts_count"]
                        }
                    }
                },
                {
                    "$sort": {"total_revenue": -1}
                }
            ]
            
            result = list(self.concerts_collection.aggregate(pipeline))
            return result
            
        except PyMongoError as e:
            print(f"Error in revenue by venue aggregation: {e}")
            return []
    
    def get_top_customers_by_spending(self, limit: int = 10) -> List[Dict]:
        """
        Get top customers by total spending.
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$customer_id",
                        "total_spent": {"$sum": "$total_amount"},
                        "total_bookings": {"$sum": 1},
                        "total_tickets": {"$sum": "$quantity"}
                    }
                },
                {
                    "$lookup": {
                        "from": CUSTOMERS_COLLECTION,
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "customer_info"
                    }
                },
                {
                    "$unwind": "$customer_info"
                },
                {
                    "$project": {
                        "_id": 0,
                        "customer_name": "$customer_info.name",
                        "customer_email": "$customer_info.email",
                        "total_spent": 1,
                        "total_bookings": 1,
                        "total_tickets": 1,
                        "avg_spending_per_booking": {
                            "$divide": ["$total_spent", "$total_bookings"]
                        }
                    }
                },
                {
                    "$sort": {"total_spent": -1}
                },
                {
                    "$limit": limit
                }
            ]
            
            result = list(self.bookings_collection.aggregate(pipeline))
            return result
            
        except PyMongoError as e:
            print(f"Error in top customers aggregation: {e}")
            return []