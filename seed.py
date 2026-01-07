from app import app
from models import db, Guest, Rooms, Reservation,User
from datetime import datetime, timedelta

def seed_data():
    with app.app_context():
        # Delete existing data
        db.session.query(Reservation).delete()
        db.session.query(Rooms).delete()
        db.session.query(Guest).delete()
        db.session.query(User).delete()
        db.session.commit()

        # Seed guests
        guests = [
            Guest(name='Alice Kimani', email='alice@example.com', phone='123456789012'),
            Guest(name='Bob Otieno', email='bob@example.com', phone='123456789013'),
            Guest(name='Cynthia Mwangi', email='cynthia@example.com', phone='123456789014'),
            Guest(name='Daniel Njoroge', email='daniel@example.com', phone='123456789015'),
            Guest(name='Eve Wanjiku', email='eve@example.com', phone='123456789016'),
            Guest(name='Frank Karanja', email='frank@example.com', phone='123456789017'),
            Guest(name='Grace Muthoni', email='grace@example.com', phone='123456789018'),
            Guest(name='Hassan Ahmed', email='hassan@example.com', phone='123456789019'),
            Guest(name='Ivy Odhiambo', email='ivy@example.com', phone='123456789020'),
            Guest(name='Jack Ochieng', email='jack@example.com', phone='123456789021')
        ]
        db.session.add_all(guests)
        db.session.commit()

        # Seed rooms with images
        rooms = [
            Rooms(room_number=101, room_type='single', price_per_night=50, status='available', image='https://images.unsplash.com/photo-1685592437742-3b56edb46b15?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            Rooms(room_number=102, room_type='double', price_per_night=75, status='available', image='https://images.unsplash.com/photo-1618773928121-c32242e63f39?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            Rooms(room_number=103, room_type='suite', price_per_night=150, status='occupied', image='https://images.unsplash.com/photo-1644057501622-dfa7dd26dbfb?q=80&w=1381&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            Rooms(room_number=104, room_type='single', price_per_night=55, status='available', image='https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzZ8fGhvdGVsJTIwcm9vbXN8ZW58MHx8MHx8fDA%3D'),
            Rooms(room_number=105, room_type='double', price_per_night=80, status='available', image='https://plus.unsplash.com/premium_photo-1684445035187-c4bc7c96bc5d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTN8fGhvdGVsJTIwcm9vbXN8ZW58MHx8MHx8fDA%3D')
        ]
        db.session.add_all(rooms)
        db.session.commit()

        # Convert datetime to string in 'YYYY-MM-DD HH:MM:SS' format
        def format_date(date_obj):
            return date_obj.strftime('%Y-%m-%d %H:%M:%S')

        # Seed reservations
        reservations = [
            Reservation(
                check_in_date=format_date(datetime.now() + timedelta(days=5)),
                check_out_date=format_date(datetime.now() + timedelta(days=10)),
                total_price=200,
                guest_id=guests[0].id,
                room_id=rooms[0].id
            ),
            Reservation(
                check_in_date=format_date(datetime.now() + timedelta(days=6)),
                check_out_date=format_date(datetime.now() + timedelta(days=11)),
                total_price=300,
                guest_id=guests[1].id,
                room_id=rooms[1].id
            ),
            Reservation(
                check_in_date=format_date(datetime.now() + timedelta(days=7)),
                check_out_date=format_date(datetime.now() + timedelta(days=12)),
                total_price=400,
                guest_id=guests[2].id,
                room_id=rooms[2].id
            )
        ]


        db.session.add_all(reservations)
        db.session.commit()

        user = [
            User(username='admin', password='admin123', role='admin'),
            User(username='Walice', password='user123', role='user')
        ]
        db.session.add_all(user)
        db.session.commit()

seed_data()