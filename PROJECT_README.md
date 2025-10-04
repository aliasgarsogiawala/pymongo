# 🎵 Concert Booking System

A full-featured concert booking web application built with Flask and MongoDB, implementing complete CRUD operations and advanced MongoDB aggregation functions.

## ✨ Features

### CRUD Operations
- **Create**: Add new concerts and bookings
- **Read**: View all concerts, bookings, and detailed analytics
- **Update**: Edit concert details and booking information
- **Delete**: Remove concerts and cancel bookings

### MongoDB Aggregation Functions
- **Revenue by Concert**: Total revenue and tickets sold per concert
- **Concert Occupancy Rates**: Real-time seat availability and occupancy percentages
- **Top Customers**: Rankings by total spend and number of bookings
- **Bookings by Status**: Breakdown of confirmed, pending, and cancelled bookings
- **Revenue by Genre**: Revenue analysis grouped by music genre
- **Monthly Revenue Trends**: Time-series analysis of booking patterns

### Modern UI
- Responsive design that works on desktop, tablet, and mobile
- Beautiful gradient navigation and card-based layouts
- Real-time form validation and dynamic calculations
- Modal dialogs for create/edit operations
- Flash messages for user feedback

## 🛠️ Technology Stack

- **Backend**: Flask 3.0.0
- **Database**: MongoDB Atlas
- **Frontend**: HTML5, CSS3, JavaScript
- **Python Libraries**:
  - `pymongo[srv]` - MongoDB driver
  - `python-dotenv` - Environment variable management
  - `flask-cors` - Cross-origin resource sharing
  - `certifi` - SSL certificate verification

## 📋 Prerequisites

- Python 3.8+
- MongoDB Atlas account (free tier works fine)
- Internet connection for MongoDB Atlas

## 🚀 Quick Start

### 1. Clone the Repository
```bash
cd /workspaces/pymongo
```

### 2. Configure Environment Variables

Your `.env.local` file should contain:
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGO_DB=concert_data
```

**Important MongoDB Atlas Setup:**
1. Go to MongoDB Atlas Dashboard
2. Navigate to Network Access
3. Add your IP address (or `0.0.0.0/0` for development)
4. Verify your database user credentials

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python init_db.py
```

This script will:
- Create necessary collections (concerts, bookings, customers)
- Set up database indexes for optimal performance
- Insert sample data (6 concerts, 4 sample bookings)

### 5. Run the Application

**Option A: Using the start script**
```bash
./start.sh
```

**Option B: Direct Python command**
```bash
python app.py
```

The application will start on `http://localhost:5000`

## 📱 Application Structure

```
/workspaces/pymongo/
├── app.py                 # Main Flask application with routes
├── config.py             # Database configuration
├── init_db.py           # Database initialization script
├── requirements.txt     # Python dependencies
├── .env.local          # Environment variables (MongoDB credentials)
├── start.sh            # Quick start script
├── templates/          # HTML templates
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Dashboard with statistics
│   ├── concerts.html      # Concert management (CRUD)
│   ├── bookings.html      # Booking management (CRUD)
│   └── analytics.html     # Analytics with aggregations
└── static/
    └── css/
        └── style.css      # Application styling
```

## 🎯 Application Pages

### 1. Dashboard (`/`)
- Overview statistics using MongoDB aggregations
- Total concerts, bookings, revenue
- Quick action buttons
- Feature highlights

### 2. Concerts Management (`/concerts`)
- **View**: Grid display of all concerts
- **Add**: Modal form to create new concerts
- **Edit**: Update concert details
- **Delete**: Remove concerts (with booking validation)
- Real-time seat availability tracking

### 3. Bookings Management (`/bookings`)
- **View**: Table display with concert details (using `$lookup`)
- **Add**: Create new bookings with live price calculation
- **Edit**: Modify booking details
- **Cancel**: Delete bookings and restore seats
- Automatic seat inventory management

### 4. Analytics (`/analytics`)
Advanced MongoDB aggregation pipelines:
- Revenue by concert with `$group` and `$sum`
- Concert occupancy using `$lookup` and `$divide`
- Top customers with `$sort` and `$limit`
- Bookings by status with conditional aggregation
- Revenue by genre using `$match` and `$group`
- Monthly trends with `$dateToString`

## 🔧 API Endpoints

### Concerts
- `GET /concerts` - List all concerts
- `POST /concerts/add` - Create new concert
- `POST /concerts/edit/<id>` - Update concert
- `POST /concerts/delete/<id>` - Delete concert
- `GET /concerts/get/<id>` - Get concert JSON (AJAX)

### Bookings
- `GET /bookings` - List all bookings
- `POST /bookings/add` - Create new booking
- `POST /bookings/edit/<id>` - Update booking
- `POST /bookings/delete/<id>` - Cancel booking
- `GET /bookings/get/<id>` - Get booking JSON (AJAX)

### Analytics
- `GET /analytics` - View all analytics dashboards

## 🔍 MongoDB Aggregation Examples

### Revenue by Concert
```python
pipeline = [
    {
        '$lookup': {
            'from': 'concerts',
            'localField': 'concert_object_id',
            'foreignField': '_id',
            'as': 'concert_details'
        }
    },
    {
        '$group': {
            '_id': '$concert_id',
            'total_revenue': {'$sum': '$total_amount'},
            'total_tickets_sold': {'$sum': '$num_tickets'}
        }
    }
]
```

### Concert Occupancy Rate
```python
pipeline = [
    {
        '$lookup': {
            'from': 'bookings',
            'localField': 'concert_id_str',
            'foreignField': 'concert_id',
            'as': 'bookings'
        }
    },
    {
        '$addFields': {
            'occupancy_rate': {
                '$multiply': [
                    {'$divide': [{'$sum': '$bookings.num_tickets'}, '$total_seats']},
                    100
                ]
            }
        }
    }
]
```

## 🐛 Troubleshooting

### MongoDB Connection Issues

**SSL Handshake Error:**
This is typically an OpenSSL version issue in the dev container. The app includes `tlsAllowInvalidCertificates=True` for development.

**IP Whitelist:**
```
1. Go to MongoDB Atlas → Network Access
2. Add your IP or 0.0.0.0/0 for development
3. Wait 1-2 minutes for changes to propagate
```

**Authentication Failed:**
- Verify username/password in `.env.local`
- Check that the database user has read/write permissions
- Ensure special characters in password are URL-encoded

### Application Won't Start
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version  # Should be 3.8+

# Verify Flask installation
python -c "import flask; print(flask.__version__)"
```

## 🎨 Customization

### Adding New Concert Genres
Edit `templates/concerts.html` and add options to the genre field.

### Changing Color Theme
Modify CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #3498db;
    --secondary-color: #2ecc71;
    /* ... */
}
```

### Adding New Aggregations
Add new pipelines in `app.py` under the `/analytics` route.

## 📊 Database Schema

### Concerts Collection
```json
{
  "_id": ObjectId,
  "name": "Concert Name",
  "artist": "Artist Name",
  "venue": "Venue Name",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "ticket_price": 125.00,
  "total_seats": 500,
  "available_seats": 450,
  "genre": "Rock",
  "description": "Concert description",
  "created_at": ISODate
}
```

### Bookings Collection
```json
{
  "_id": ObjectId,
  "concert_id": "concert_object_id_as_string",
  "customer_name": "Customer Name",
  "customer_email": "email@example.com",
  "customer_phone": "555-0100",
  "num_tickets": 2,
  "ticket_price": 125.00,
  "total_amount": 250.00,
  "booking_date": ISODate,
  "status": "confirmed"
}
```

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

## 📝 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Built with ❤️ using Flask and MongoDB

## 🎉 Acknowledgments

- Flask framework for the awesome Python web framework
- MongoDB for the powerful database and aggregation pipeline
- Font Awesome for beautiful icons
- GitHub Codespaces for the development environment

---

**Happy Coding! 🚀**
