# 🎵 Concert Booking System - CRUD & Aggregation Operations
**Built by Aliasgar Sogiawala**

## 📋 **COMPLETE LIST OF CRUD AND AGGREGATION OPERATIONS**

### **CRUD OPERATIONS**

#### **1. Concert CRUD (ConcertCRUD class)**
- **CREATE**: `create_concert()` - Insert new concert documents using `insert_one()`
- **READ**: 
  - `get_concert()` - Find concert by ID using `find_one({"_id": concert_id})`
  - `get_all_concerts()` - Find all concerts using `find()`
- **UPDATE**: 
  - `update_concert()` - Update concert fields using `update_one({"_id": id}, {"$set": data})`
  - `update_available_seats()` - Increment/decrement seats using `update_one()` with `$inc`
- **DELETE**: `delete_concert()` - Remove concert documents using `delete_one({"_id": id})`

#### **2. Customer CRUD (CustomerCRUD class)**
- **CREATE**: `create_customer()` - Insert new customer documents using `insert_one()`
- **READ**: 
  - `get_customer()` - Find customer by ID using `find_one({"_id": customer_id})`
  - `get_customer_by_email()` - Find customer by email using `find_one({"email": email})`
  - `get_all_customers()` - Find all customers using `find()`
- **UPDATE**: `update_customer()` - Update customer fields using `update_one()` with `$set`
- **DELETE**: `delete_customer()` - Remove customer documents using `delete_one()`

#### **3. Booking CRUD (BookingCRUD class)**
- **CREATE**: `create_booking()` - Insert new booking documents using `insert_one()`
- **READ**: 
  - `get_booking()` - Find booking by ID using `find_one({"_id": booking_id})`
  - `get_bookings_by_customer()` - Find bookings by customer using `find({"customer_id": id})`
  - `get_bookings_by_concert()` - Find bookings by concert using `find({"concert_id": id})`
  - `get_all_bookings()` - Find all bookings using `find()`
- **UPDATE**: 
  - `update_booking()` - Update booking fields using `update_one()` with `$set`
  - `cancel_booking()` - Mark booking as cancelled using `update_one()`
- **DELETE**: `delete_booking()` - Remove booking documents using `delete_one()`

#### **4. Invoice CRUD (InvoiceCRUD class)**
- **CREATE**: `create_invoice()` - Insert new invoice documents using `insert_one()`
- **READ**: 
  - `get_invoice()` - Find invoice by ID using `find_one({"_id": invoice_id})`
  - `get_invoice_by_booking()` - Find invoice by booking ID using `find_one({"booking_id": id})`
  - `get_invoices_by_customer()` - Find invoices by customer using `find({"customer_id": id})`
  - `get_all_invoices()` - Find all invoices using `find()`
- **UPDATE**: 
  - `update_invoice()` - Update invoice fields using `update_one()` with `$set`
  - `mark_paid()` - Mark invoice as paid using `update_one()`
- **DELETE**: `delete_invoice()` - Remove invoice documents using `delete_one()`

---

### **AGGREGATION OPERATIONS**

#### **1. Revenue Analytics**

##### **Revenue by Concert**
```javascript
pipeline = [
    {
        "$addFields": {
            "concert_object_id": {"$toObjectId": "$concert_id"}
        }
    },
    {
        "$lookup": {
            "from": "concerts",
            "localField": "concert_object_id", 
            "foreignField": "_id",
            "as": "concert_details"
        }
    },
    {
        "$unwind": "$concert_details"
    },
    {
        "$group": {
            "_id": "$concert_id",
            "concert_name": {"$first": "$concert_details.name"},
            "artist": {"$first": "$concert_details.artist"},
            "total_revenue": {"$sum": "$total_amount"},
            "total_tickets_sold": {"$sum": "$num_tickets"},
            "total_bookings": {"$sum": 1}
        }
    },
    {
        "$sort": {"total_revenue": -1}
    }
]
```

##### **Revenue by Venue**
```javascript
pipeline = [
    {
        "$lookup": {
            "from": "bookings",
            "localField": "_id",
            "foreignField": "concert_id", 
            "as": "bookings"
        }
    },
    {
        "$unwind": {"path": "$bookings", "preserveNullAndEmptyArrays": true}
    },
    {
        "$group": {
            "_id": "$venue",
            "total_revenue": {"$sum": "$bookings.total_amount"},
            "total_concerts": {"$addToSet": "$_id"},
            "total_tickets_sold": {"$sum": "$bookings.quantity"}
        }
    }
]
```

##### **Revenue by Genre**
```javascript
pipeline = [
    {
        "$lookup": {
            "from": "concerts",
            "localField": "concert_object_id",
            "foreignField": "_id",
            "as": "concert_details"
        }
    },
    {
        "$group": {
            "_id": "$concert_details.genre",
            "total_revenue": {"$sum": "$total_amount"},
            "total_bookings": {"$sum": 1},
            "avg_ticket_price": {"$avg": "$ticket_price"}
        }
    }
]
```

##### **Monthly Revenue Trends**
```javascript
pipeline = [
    {
        "$addFields": {
            "month_year": {
                "$dateToString": {
                    "format": "%Y-%m",
                    "date": "$booking_date"
                }
            }
        }
    },
    {
        "$group": {
            "_id": "$month_year",
            "total_revenue": {"$sum": "$total_amount"},
            "total_bookings": {"$sum": 1}
        }
    },
    {
        "$sort": {"_id": 1}
    }
]
```

#### **2. Customer Analytics**

##### **Customer Booking Statistics**
```javascript
pipeline = [
    {
        "$lookup": {
            "from": "bookings",
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
        "$match": {"total_bookings": {"$gt": 0}}
    }
]
```

##### **Top Customers by Spending**
```javascript
pipeline = [
    {
        "$group": {
            "_id": "$customer_email",
            "customer_name": {"$first": "$customer_name"},
            "total_bookings": {"$sum": 1},
            "total_spent": {"$sum": "$total_amount"},
            "total_tickets": {"$sum": "$num_tickets"}
        }
    },
    {
        "$sort": {"total_spent": -1}
    },
    {
        "$limit": 10
    }
]
```

#### **3. Concert Analytics**

##### **Popular Concerts**
```javascript
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
            "from": "concerts",
            "localField": "_id",
            "foreignField": "_id",
            "as": "concert_info"
        }
    },
    {
        "$addFields": {
            "unique_customers_count": {"$size": "$unique_customers"}
        }
    }
]
```

##### **Concert Occupancy Rates**
```javascript
pipeline = [
    {
        "$addFields": {
            "concert_id_str": {"$toString": "$_id"}
        }
    },
    {
        "$lookup": {
            "from": "bookings",
            "localField": "concert_id_str",
            "foreignField": "concert_id",
            "as": "bookings"
        }
    },
    {
        "$addFields": {
            "tickets_sold": {"$sum": "$bookings.num_tickets"},
            "occupancy_rate": {
                "$multiply": [
                    {"$divide": [{"$sum": "$bookings.num_tickets"}, "$total_seats"]},
                    100
                ]
            }
        }
    }
]
```

##### **Ticket Type Distribution**
```javascript
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
        "$sort": {"total_revenue": -1}
    }
]
```

#### **4. Booking Analytics**

##### **Bookings by Status**
```javascript
pipeline = [
    {
        "$group": {
            "_id": "$status",
            "count": {"$sum": 1},
            "total_amount": {"$sum": "$total_amount"}
        }
    },
    {
        "$sort": {"total_amount": -1}
    }
]
```

##### **Payment Status Summary**
```javascript
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
        "$sort": {"total_amount": -1}
    }
]
```

#### **5. Flask App Aggregations**

##### **Home Dashboard Statistics**
- Total concerts: `count_documents({})`
- Total bookings: `count_documents({})`
- Total revenue: Aggregation pipeline with `$group` and `$sum`
- Upcoming concerts: `count_documents({"date": {"$gte": current_date}})`

##### **Bookings with Concert Details (Join)**
```javascript
pipeline = [
    {
        "$addFields": {
            "concert_object_id": {"$toObjectId": "$concert_id"}
        }
    },
    {
        "$lookup": {
            "from": "concerts",
            "localField": "concert_object_id",
            "foreignField": "_id", 
            "as": "concert_details"
        }
    },
    {
        "$unwind": {
            "path": "$concert_details",
            "preserveNullAndEmptyArrays": true
        }
    },
    {
        "$sort": {"booking_date": -1}
    }
]
```

---

## 🔧 **MongoDB Operations Used**

### **Basic CRUD**
- `insert_one()` - Create single documents
- `insert_many()` - Create multiple documents
- `find()` - Read multiple documents
- `find_one()` - Read single document
- `update_one()` - Update single document
- `update_many()` - Update multiple documents
- `delete_one()` - Delete single document
- `delete_many()` - Delete multiple documents
- `count_documents()` - Count documents

### **Aggregation Operators**
- `$group` - Group documents by specified fields
- `$lookup` - Left outer join between collections
- `$unwind` - Deconstruct array fields
- `$match` - Filter documents
- `$project` - Include/exclude fields
- `$sort` - Sort documents
- `$limit` - Limit number of documents
- `$addFields` - Add computed fields
- `$sum` - Calculate totals
- `$avg` - Calculate averages
- `$size` - Get array size
- `$divide` - Division operation
- `$multiply` - Multiplication operation
- `$addToSet` - Add unique values to set
- `$dateToString` - Format dates as strings
- `$toObjectId` - Convert string to ObjectId
- `$toString` - Convert ObjectId to string
- `$round` - Round numbers
- `$cond` - Conditional expressions
- `$eq` - Equality comparison
- `$gt` - Greater than comparison
- `$gte` - Greater than or equal comparison
- `$inc` - Increment values
- `$set` - Set field values

---

**Built by Aliasgar Sogiawala** 🚀
