#!/usr/bin/env python3

from models import db, Guest, Rooms, Reservation, User
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'hotel.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "super-secret-key")
CORS(app)
# Initialize JWT
jwt = JWTManager(app)

# Initialize SQLAlchemy
db.init_app(app)

# Initialize Flask-Migrate after db is initialized
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>Welcome to Hotel Management System</h1>'

# User Registration (Admin only)
@app.route('/register', methods=['POST'])
# @jwt_required()
def register_user():
    # current_user = get_jwt_identity()
    # user = User.query.filter_by(username=current_user).first()
    
    # Check if current user is an admin
    # if user.role != 'admin':
    #     return jsonify({"error": "Only admins can register new users"}), 403

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role','user')

    if not username or not password or not role:
        return jsonify({"error": "Missing data"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=username, role=role)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200








# CRUD for Guests
@app.route('/guests', methods=['GET'])
@jwt_required()
def get_guests():
    guests = Guest.query.all()
    response_data = [guest.to_dict() for guest in guests]
    return make_response(jsonify(response_data), 200)

@app.route('/guests/<int:id>', methods=['GET'])
@jwt_required()
def get_guest(id):
    guest = db.session.get(Guest, id)
    if guest:
        return make_response(jsonify(guest.to_dict()), 200)
    return jsonify({'error': 'Guest not found'}), 404

@app.route('/guests', methods=['POST'])
@jwt_required()
def create_guest():
    data = request.get_json()
    # print("getting data...",data)
    try:
        new_guest = Guest(
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )
        db.session.add(new_guest)
        db.session.commit()
        return make_response(jsonify(new_guest.to_dict()), 201)
    except Exception as e:
        # print("Getting error",str(e))
        return jsonify({'error': str(e)}), 400

@app.route('/guests/<int:id>', methods=['PATCH'], endpoint='update_guest')
@jwt_required()
def update_guest(id):
    guest = db.session.get(Guest, id)
    if not guest:
        return jsonify({'error': 'Guest not found'}), 404

    data = request.get_json()
    if 'name' in data:
        guest.name = data['name']
    if 'email' in data:
        try:
            guest.email = data['email']
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    if 'phone' in data:
        try:
            guest.phone = data['phone']
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    db.session.commit()
    return make_response(jsonify(guest.to_dict()), 200)

@app.route('/guests/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_guest(id):
    guest = db.session.get(Guest, id)
    if not guest:
        return jsonify({'error': 'Guest not found'}), 404
    db.session.delete(guest)
    db.session.commit()
    return make_response({'message': 'Guest deleted'}, 202)

# CRUD for Rooms
@app.route('/rooms', methods=['GET'])
@jwt_required()
def get_all():
    rooms = Rooms.query.all()
    return jsonify([room.to_dict() for room in rooms])
@jwt_required()
def get_rooms():
    rooms = Rooms.query.all()
    response_data = [room.to_dict() for room in rooms]
    return make_response(jsonify(response_data), 200)

@app.route('/rooms/<int:id>', methods=['GET'])
@jwt_required()
def get_room(id):
    room = db.session.get(Rooms, id)
    if room:
        return jsonify(room.to_dict()), 200
    return jsonify({'error': 'Room not found'}), 404

@app.route('/rooms', methods=['POST'])
@jwt_required()
def create_room():
    data = request.get_json()
    try:
        new_room = Rooms(
            room_number=data['room_number'],
            room_type=data['room_type'],
            price_per_night=data['price_per_night'],
            status=data['status']
        )
        db.session.add(new_room)
        db.session.commit()
        return make_response(jsonify(new_room.to_dict()), 201)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/rooms/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_room(id):
    room = db.session.get(Rooms, id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    db.session.delete(room)
    db.session.commit()
    return make_response({'message': 'room deleted successfully'}, 202)

# CRUD for Reservations
@app.route('/reservations', methods=['GET'])
@jwt_required()
def get_reservations():
    reservations = Reservation.query.all()
    response_data = [reservation.to_dict() for reservation in reservations]
    print(response_data)
    return make_response(jsonify(response_data), 200)

@app.route('/reservations/<int:id>', methods=['GET'])
@jwt_required()
def get_reservation(id):
    reservation = db.session.get(Reservation, id)
    if reservation:
        return jsonify(reservation.to_dict()), 200
    return jsonify({'error': 'Reservation not found'}), 404

@app.route('/reservations', methods=['POST'])
@jwt_required()
def create_reservation():
    data = request.get_json()
    # print("Incoming data..",data)
    try:
        new_reservation = Reservation(
            check_in_date=data['check_in_date'],
            check_out_date=data['check_out_date'],
            total_price=data['total_price'],
            guest_id=data['guest_id'],
            room_id=data['room_id']
        )
        db.session.add(new_reservation)
        db.session.commit()
        return make_response(jsonify(new_reservation.to_dict()), 201)
    except Exception as e:
        # print("Here is the Error",str(e))
        return jsonify({'error': str(e)}), 400

@app.route('/reservations/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_reservation(id):
    reservation = db.session.get(Reservation, id)
    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404
    db.session.delete(reservation)
    db.session.commit()
    return make_response({'message': 'Reservation successfully deleted'}, 202)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5555)) 
    app.run(host="0.0.0.0", port=port,debug=True)