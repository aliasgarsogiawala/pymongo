# MongoDB Schema Documentation

This project uses MongoDB as its database. MongoDB is a NoSQL, document-oriented database. Below is a sample schema for the collections used in this project. Adjust as needed for your application.

---

## Example Collection: users

```
{
  _id: ObjectId,           // MongoDB unique identifier
  username: String,        // Unique username
  email: String,           // User email address
  password_hash: String,   // Hashed password
  created_at: Date,        // Account creation date
  is_active: Boolean       // User status
}
```

## Example Collection: invoices

```
{
  _id: ObjectId,
  user_id: ObjectId,       // Reference to users collection
  amount: Number,          // Invoice amount
  status: String,          // e.g., 'paid', 'unpaid', 'pending'
  issued_at: Date,         // Invoice issue date
  due_date: Date           // Invoice due date
}
```

---

# How to Use
- Copy `.env.example` to `.env` and fill in your MongoDB credentials.
- Collections and fields can be modified as per your requirements.
- Use the above schema as a guideline for your MongoDB documents.
