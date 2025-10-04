"""
Concert Booking System - Flask Application
Implements CRUD operations and MongoDB aggregate functions
"""
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from config import get_database
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'concert-booking-secret-key-2025')

# Get database connection
db = get_database()
concerts_collection = db['concerts']
bookings_collection = db['bookings']
customers_collection = db['customers']

# ==================== HOME PAGE ====================
@app.route('/')
def index():
    """Home page with overview statistics using aggregation"""
    try:
        # Aggregate: Total concerts
        total_concerts = concerts_collection.count_documents({})
        
        # Aggregate: Total bookings
        total_bookings = bookings_collection.count_documents({})
        
        # Aggregate: Total revenue using aggregation pipeline
        revenue_pipeline = [
            {
                '$group': {
                    '_id': None,
                    'total_revenue': {'$sum': '$total_amount'}
                }
            }
        ]
        revenue_result = list(bookings_collection.aggregate(revenue_pipeline))
        total_revenue = revenue_result[0]['total_revenue'] if revenue_result else 0
        
        # Aggregate: Upcoming concerts count
        upcoming_concerts = concerts_collection.count_documents({
            'date': {'$gte': datetime.now().strftime('%Y-%m-%d')}
        })
        
        stats = {
            'total_concerts': total_concerts,
            'total_bookings': total_bookings,
            'total_revenue': total_revenue,
            'upcoming_concerts': upcoming_concerts
        }
        
        return render_template('index.html', stats=stats)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('index.html', stats={})

# ==================== CONCERTS CRUD ====================
@app.route('/concerts')
def concerts():
    """List all concerts"""
    try:
        all_concerts = list(concerts_collection.find().sort('date', 1))
        return render_template('concerts.html', concerts=all_concerts)
    except Exception as e:
        flash(f'Error loading concerts: {str(e)}', 'error')
        return render_template('concerts.html', concerts=[])

@app.route('/concerts/add', methods=['POST'])
def add_concert():
    """Create a new concert"""
    try:
        concert_data = {
            'name': request.form.get('name'),
            'artist': request.form.get('artist'),
            'venue': request.form.get('venue'),
            'date': request.form.get('date'),
            'time': request.form.get('time'),
            'ticket_price': float(request.form.get('ticket_price', 0)),
            'total_seats': int(request.form.get('total_seats', 0)),
            'available_seats': int(request.form.get('total_seats', 0)),
            'genre': request.form.get('genre', ''),
            'description': request.form.get('description', ''),
            'created_at': datetime.now()
        }
        
        result = concerts_collection.insert_one(concert_data)
        flash(f'Concert "{concert_data["name"]}" added successfully!', 'success')
        return redirect(url_for('concerts'))
    except Exception as e:
        flash(f'Error adding concert: {str(e)}', 'error')
        return redirect(url_for('concerts'))

@app.route('/concerts/edit/<concert_id>', methods=['POST'])
def edit_concert(concert_id):
    """Update an existing concert"""
    try:
        update_data = {
            'name': request.form.get('name'),
            'artist': request.form.get('artist'),
            'venue': request.form.get('venue'),
            'date': request.form.get('date'),
            'time': request.form.get('time'),
            'ticket_price': float(request.form.get('ticket_price', 0)),
            'total_seats': int(request.form.get('total_seats', 0)),
            'genre': request.form.get('genre', ''),
            'description': request.form.get('description', ''),
            'updated_at': datetime.now()
        }
        
        result = concerts_collection.update_one(
            {'_id': ObjectId(concert_id)},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            flash('Concert updated successfully!', 'success')
        else:
            flash('No changes made to concert.', 'info')
        
        return redirect(url_for('concerts'))
    except Exception as e:
        flash(f'Error updating concert: {str(e)}', 'error')
        return redirect(url_for('concerts'))

@app.route('/concerts/delete/<concert_id>', methods=['POST'])
def delete_concert(concert_id):
    """Delete a concert"""
    try:
        # Check if there are bookings for this concert
        booking_count = bookings_collection.count_documents({'concert_id': concert_id})
        
        if booking_count > 0:
            flash(f'Cannot delete concert with {booking_count} existing bookings!', 'error')
        else:
            result = concerts_collection.delete_one({'_id': ObjectId(concert_id)})
            if result.deleted_count > 0:
                flash('Concert deleted successfully!', 'success')
            else:
                flash('Concert not found!', 'error')
        
        return redirect(url_for('concerts'))
    except Exception as e:
        flash(f'Error deleting concert: {str(e)}', 'error')
        return redirect(url_for('concerts'))

@app.route('/concerts/get/<concert_id>')
def get_concert(concert_id):
    """Get concert details (for AJAX requests)"""
    try:
        concert = concerts_collection.find_one({'_id': ObjectId(concert_id)})
        if concert:
            concert['_id'] = str(concert['_id'])
            return jsonify(concert)
        return jsonify({'error': 'Concert not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== BOOKINGS CRUD ====================
@app.route('/bookings')
def bookings():
    """List all bookings with concert details using aggregation"""
    try:
        # Aggregate: Join bookings with concerts using $lookup
        pipeline = [
            {
                '$addFields': {
                    'concert_object_id': {'$toObjectId': '$concert_id'}
                }
            },
            {
                '$lookup': {
                    'from': 'concerts',
                    'localField': 'concert_object_id',
                    'foreignField': '_id',
                    'as': 'concert_details'
                }
            },
            {
                '$unwind': {
                    'path': '$concert_details',
                    'preserveNullAndEmptyArrays': True
                }
            },
            {
                '$sort': {'booking_date': -1}
            }
        ]
        
        all_bookings = list(bookings_collection.aggregate(pipeline))
        all_concerts = list(concerts_collection.find())
        
        return render_template('bookings.html', bookings=all_bookings, concerts=all_concerts)
    except Exception as e:
        flash(f'Error loading bookings: {str(e)}', 'error')
        return render_template('bookings.html', bookings=[], concerts=[])

@app.route('/bookings/add', methods=['POST'])
def add_booking():
    """Create a new booking"""
    try:
        concert_id = request.form.get('concert_id')
        num_tickets = int(request.form.get('num_tickets', 1))
        
        # Get concert details
        concert = concerts_collection.find_one({'_id': ObjectId(concert_id)})
        
        if not concert:
            flash('Concert not found!', 'error')
            return redirect(url_for('bookings'))
        
        # Check available seats
        if concert['available_seats'] < num_tickets:
            flash(f'Only {concert["available_seats"]} seats available!', 'error')
            return redirect(url_for('bookings'))
        
        # Calculate total amount
        total_amount = concert['ticket_price'] * num_tickets
        
        # Create booking
        booking_data = {
            'concert_id': concert_id,
            'customer_name': request.form.get('customer_name'),
            'customer_email': request.form.get('customer_email'),
            'customer_phone': request.form.get('customer_phone'),
            'num_tickets': num_tickets,
            'ticket_price': concert['ticket_price'],
            'total_amount': total_amount,
            'booking_date': datetime.now(),
            'status': 'confirmed'
        }
        
        # Insert booking
        result = bookings_collection.insert_one(booking_data)
        
        # Update available seats
        concerts_collection.update_one(
            {'_id': ObjectId(concert_id)},
            {'$inc': {'available_seats': -num_tickets}}
        )
        
        flash(f'Booking confirmed! Total: ${total_amount:.2f}', 'success')
        return redirect(url_for('bookings'))
    except Exception as e:
        flash(f'Error creating booking: {str(e)}', 'error')
        return redirect(url_for('bookings'))

@app.route('/bookings/edit/<booking_id>', methods=['POST'])
def edit_booking(booking_id):
    """Update an existing booking"""
    try:
        booking = bookings_collection.find_one({'_id': ObjectId(booking_id)})
        
        if not booking:
            flash('Booking not found!', 'error')
            return redirect(url_for('bookings'))
        
        old_num_tickets = booking['num_tickets']
        new_num_tickets = int(request.form.get('num_tickets', 1))
        ticket_difference = new_num_tickets - old_num_tickets
        
        # Get concert
        concert = concerts_collection.find_one({'_id': ObjectId(booking['concert_id'])})
        
        # Check if we have enough seats
        if ticket_difference > 0 and concert['available_seats'] < ticket_difference:
            flash(f'Only {concert["available_seats"]} additional seats available!', 'error')
            return redirect(url_for('bookings'))
        
        # Calculate new total
        new_total = concert['ticket_price'] * new_num_tickets
        
        # Update booking
        update_data = {
            'customer_name': request.form.get('customer_name'),
            'customer_email': request.form.get('customer_email'),
            'customer_phone': request.form.get('customer_phone'),
            'num_tickets': new_num_tickets,
            'total_amount': new_total,
            'status': request.form.get('status', 'confirmed'),
            'updated_at': datetime.now()
        }
        
        bookings_collection.update_one(
            {'_id': ObjectId(booking_id)},
            {'$set': update_data}
        )
        
        # Update concert seats
        concerts_collection.update_one(
            {'_id': ObjectId(booking['concert_id'])},
            {'$inc': {'available_seats': -ticket_difference}}
        )
        
        flash('Booking updated successfully!', 'success')
        return redirect(url_for('bookings'))
    except Exception as e:
        flash(f'Error updating booking: {str(e)}', 'error')
        return redirect(url_for('bookings'))

@app.route('/bookings/delete/<booking_id>', methods=['POST'])
def delete_booking(booking_id):
    """Delete a booking (cancel)"""
    try:
        booking = bookings_collection.find_one({'_id': ObjectId(booking_id)})
        
        if not booking:
            flash('Booking not found!', 'error')
            return redirect(url_for('bookings'))
        
        # Delete booking
        bookings_collection.delete_one({'_id': ObjectId(booking_id)})
        
        # Restore seats
        concerts_collection.update_one(
            {'_id': ObjectId(booking['concert_id'])},
            {'$inc': {'available_seats': booking['num_tickets']}}
        )
        
        flash('Booking cancelled successfully!', 'success')
        return redirect(url_for('bookings'))
    except Exception as e:
        flash(f'Error cancelling booking: {str(e)}', 'error')
        return redirect(url_for('bookings'))

@app.route('/bookings/get/<booking_id>')
def get_booking(booking_id):
    """Get booking details (for AJAX requests)"""
    try:
        booking = bookings_collection.find_one({'_id': ObjectId(booking_id)})
        if booking:
            booking['_id'] = str(booking['_id'])
            return jsonify(booking)
        return jsonify({'error': 'Booking not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ANALYTICS (Aggregate Functions) ====================
@app.route('/analytics')
def analytics():
    """Analytics page with various MongoDB aggregate functions"""
    try:
        # 1. Revenue by Concert
        revenue_by_concert = list(bookings_collection.aggregate([
            {
                '$addFields': {
                    'concert_object_id': {'$toObjectId': '$concert_id'}
                }
            },
            {
                '$lookup': {
                    'from': 'concerts',
                    'localField': 'concert_object_id',
                    'foreignField': '_id',
                    'as': 'concert_details'
                }
            },
            {
                '$unwind': '$concert_details'
            },
            {
                '$group': {
                    '_id': '$concert_id',
                    'concert_name': {'$first': '$concert_details.name'},
                    'artist': {'$first': '$concert_details.artist'},
                    'total_revenue': {'$sum': '$total_amount'},
                    'total_tickets_sold': {'$sum': '$num_tickets'},
                    'total_bookings': {'$sum': 1}
                }
            },
            {
                '$sort': {'total_revenue': -1}
            }
        ]))
        
        # 2. Bookings by Status
        bookings_by_status = list(bookings_collection.aggregate([
            {
                '$group': {
                    '_id': '$status',
                    'count': {'$sum': 1},
                    'total_amount': {'$sum': '$total_amount'}
                }
            },
            {
                '$sort': {'total_amount': -1}
            }
        ]))
        
        # 3. Top Customers
        top_customers = list(bookings_collection.aggregate([
            {
                '$group': {
                    '_id': '$customer_email',
                    'customer_name': {'$first': '$customer_name'},
                    'total_bookings': {'$sum': 1},
                    'total_spent': {'$sum': '$total_amount'},
                    'total_tickets': {'$sum': '$num_tickets'}
                }
            },
            {
                '$sort': {'total_spent': -1}
            },
            {
                '$limit': 10
            }
        ]))
        
        # 4. Concert Occupancy Rate
        concert_occupancy = list(concerts_collection.aggregate([
            {
                '$addFields': {
                    'concert_id_str': {'$toString': '$_id'}
                }
            },
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
                    'tickets_sold': {
                        '$sum': '$bookings.num_tickets'
                    },
                    'available_seats': {
                        '$subtract': ['$total_seats', {'$sum': '$bookings.num_tickets'}]
                    },
                    'occupancy_rate': {
                        '$cond': {
                            'if': {'$eq': ['$total_seats', 0]},
                            'then': 0,
                            'else': {
                                '$multiply': [
                                    {
                                        '$divide': [
                                            {'$sum': '$bookings.num_tickets'},
                                            '$total_seats'
                                        ]
                                    },
                                    100
                                ]
                            }
                        }
                    }
                }
            },
            {
                '$project': {
                    'name': 1,
                    'artist': 1,
                    'venue': 1,
                    'date': 1,
                    'total_seats': 1,
                    'available_seats': 1,
                    'tickets_sold': 1,
                    'occupancy_rate': {'$round': ['$occupancy_rate', 1]}
                }
            },
            {
                '$sort': {'occupancy_rate': -1}
            }
        ]))
        
        # 5. Revenue by Genre
        revenue_by_genre = list(bookings_collection.aggregate([
            {
                '$addFields': {
                    'concert_object_id': {'$toObjectId': '$concert_id'}
                }
            },
            {
                '$lookup': {
                    'from': 'concerts',
                    'localField': 'concert_object_id',
                    'foreignField': '_id',
                    'as': 'concert_details'
                }
            },
            {
                '$unwind': '$concert_details'
            },
            {
                '$group': {
                    '_id': '$concert_details.genre',
                    'total_revenue': {'$sum': '$total_amount'},
                    'total_bookings': {'$sum': 1},
                    'avg_ticket_price': {'$avg': '$ticket_price'}
                }
            },
            {
                '$sort': {'total_revenue': -1}
            }
        ]))
        
        # 6. Monthly Revenue Trend
        monthly_revenue = list(bookings_collection.aggregate([
            {
                '$addFields': {
                    'month_year': {
                        '$dateToString': {
                            'format': '%Y-%m',
                            'date': '$booking_date'
                        }
                    }
                }
            },
            {
                '$group': {
                    '_id': '$month_year',
                    'total_revenue': {'$sum': '$total_amount'},
                    'total_bookings': {'$sum': 1}
                }
            },
            {
                '$sort': {'_id': 1}
            }
        ]))
        
        analytics_data = {
            'revenue_by_concert': revenue_by_concert,
            'bookings_by_status': bookings_by_status,
            'top_customers': top_customers,
            'concert_occupancy': concert_occupancy,
            'revenue_by_genre': revenue_by_genre,
            'monthly_revenue': monthly_revenue
        }
        
        return render_template('analytics.html', data=analytics_data)
    except Exception as e:
        print(f"Analytics error: {str(e)}")
        flash(f'Error loading analytics: {str(e)}', 'error')
        return render_template('analytics.html', data={})

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
