# Hotel Reservation System Backend
## Overview
Welcome to the Hotel Reservation System backend! This application is built to manage reservations for a hotel. It includes features for adding and managing guests, rooms, and reservations.

## Tech Stack
- **Python**: Core programming language.

- **Flask**: Web framework for building the server-side application.

- **Flask-SQLAlchemy**: ORM for managing database interactions.

- **Flask-Migrate**: Handles database migrations.

- **SQLite**: Database management system.

## Getting Started
### Prerequisites
- Python 3.8 or higher

- Flask

- Flask-SQLAlchemy

- Flask-Migrate

- SQLAlchemy-Serializer

### Setup
1.Clone the repository:
- git clone https://github.com/your-repo/hotel-reservation-system.git
cd hotel-reservation-system
2. Create and activate a virtual environment:
- python -m venv venv
source venv/bin/activate
3. Install dependencies:
- pip install -r requirements.txt
4. Initialize and upgrade the database:
- flask db init
- flask db migrate -m "Initial migration."
- flask db upgrade
5. Seed the database with initial data:
- python seed.py
## Running the Application
### Start the Flask server:
flask run
The application will be running at http://127.0.0.1:5000/.

## Project Structure

.
├── app.py              # Main application entry point
├── models.py           # Database models and validation
├── seed.py             # Script for seeding the database
├── requirements.txt    # Python dependencies
└── migrations/         # Database migrations
## API Endpoints
### Guests
- GET /guests: Retrieve all guests.

- POST /guests: Create a new guest.

- GET /guests/<id>: Retrieve a guest by ID.

- PUT /guests/<id>: Update a guest by ID.

- DELETE /guests/<id>: Delete a guest by ID.

### Rooms
- GET /rooms: Retrieve all rooms.

- POST /rooms: Create a new room.

- GET /rooms/<id>: Retrieve a room by ID.

- PUT /rooms/<id>: Update a room by ID.

- DELETE /rooms/<id>: Delete a room by ID.

### Reservations
- GET /reservations: Retrieve all reservations.

- POST /reservations: Create a new reservation.

- GET /reservations/<id>: Retrieve a reservation by ID.

- PUT /reservations/<id>: Update a reservation by ID.

- DELETE /reservations/<id>: Delete a reservation by ID.

## Contributing
1. Fork the repository.

2. Create a new branch (git checkout -b feature-branch).

3. Make your changes.

4. Commit your changes (git commit -m 'Add new feature').

5. Push to the branch (git push origin feature-branch).

6. Open a Pull Request.

### License
This project is licensed under the MIT License.


### Authors 
1. Jeremy Gitau 
2. Tony Maina 
3. Keith Mwai 
4. Elvis Kimani
5. Franklin Ndegwa 




