"""
Grand Hotel
Application Constants & Default Seed Data
"""

# ============================================================
# ROLES
# ============================================================

ROLE_SUPERADMIN_ID = 1
ROLE_MANAGER_ID = 2
ROLE_STAFF_ID = 3
ROLE_GUEST_ID = 4


DEFAULT_ROLES = [
    {
        "id": ROLE_SUPERADMIN_ID,
        "name": "SUPERADMIN",
        # "description": "Full system administrator access",
    },
    {
        "id": ROLE_MANAGER_ID,
        "name": "MANAGER",
        # "description": "Hotel management and operational access",
    },
    {
        "id": ROLE_STAFF_ID,
        "name": "STAFF",
        # "description": "Hotel staff operational access",
    },
    {
        "id": ROLE_GUEST_ID,
        "name": "GUEST",
        # "description": "Normal hotel customer account",
    },
]


# ============================================================
# PERMISSIONS
# ============================================================

DEFAULT_PERMISSIONS = [
    # ========================================================
    # GUESTS
    # ========================================================
    {
        "id": 1,
        "name": "guest.create",
        "description": "Create guest profiles",
        "category": "guests",
    },
    {
        "id": 2,
        "name": "guest.edit",
        "description": "Edit guest details",
        "category": "guests",
    },
    {
        "id": 3,
        "name": "guest.view_all",
        "description": "View all guests",
        "category": "guests",
    },
    {
        "id": 4,
        "name": "guest_view",
        "description": "View a single guest profile",
        "category": "guests",
    },
    # ========================================================
    # MANAGERS
    # ========================================================
    {
        "id": 5,
        "name": "manager.create",
        "description": "Create manager accounts",
        "category": "managers",
    },
    {
        "id": 6,
        "name": "manager.update",
        "description": "Edit manager details",
        "category": "managers",
    },
    {
        "id": 7,
        "name": "manager.view_all",
        "description": "View all managers",
        "category": "managers",
    },
    {
        "id": 8,
        "name": "manager.view_one",
        "description": "View a single manager",
        "category": "managers",
    },
    # ========================================================
    # ROLES & PERMISSIONS
    # ========================================================
    {
        "id": 9,
        "name": "permissions.edit",
        "description": "Edit individual permissions",
        "category": "roles",
    },
    {
        "id": 10,
        "name": "permissions.manage",
        "description": "Manage role-permission assignments",
        "category": "roles",
    },
    {
        "id": 11,
        "name": "roles.create",
        "description": "Create roles",
        "category": "roles",
    },
    {
        "id": 12,
        "name": "roles.edit",
        "description": "Edit roles",
        "category": "roles",
    },
    {
        "id": 13,
        "name": "roles.view",
        "description": "View roles",
        "category": "roles",
    },
    # ========================================================
    # RESERVATIONS
    # ========================================================
    {
        "id": 14,
        "name": "reservations.cancel",
        "description": "Cancel reservations",
        "category": "reservations",
    },
    {
        "id": 15,
        "name": "reservations.check_in",
        "description": "Check guests in",
        "category": "reservations",
    },
    {
        "id": 16,
        "name": "reservations.check_out",
        "description": "Check guests out",
        "category": "reservations",
    },
    {
        "id": 17,
        "name": "reservations.confirm",
        "description": "Confirm reservations",
        "category": "reservations",
    },
    {
        "id": 18,
        "name": "reservations.create",
        "description": "Create reservations",
        "category": "reservations",
    },
    {
        "id": 19,
        "name": "reservations.edit",
        "description": "Edit reservation details",
        "category": "reservations",
    },
    {
        "id": 20,
        "name": "reservations.view_all",
        "description": "View all reservations",
        "category": "reservations",
    },
    {
        "id": 21,
        "name": "reservations.view_own",
        "description": "View own reservations",
        "category": "reservations",
    },
    # ========================================================
    # ROOMS
    # ========================================================
    {
        "id": 22,
        "name": "room.create",
        "description": "Create rooms",
        "category": "rooms",
    },
    {
        "id": 23,
        "name": "room.update",
        "description": "Edit room details",
        "category": "rooms",
    },
    {
        "id": 24,
        "name": "room.view_all",
        "description": "View all rooms",
        "category": "rooms",
    },
    {
        "id": 25,
        "name": "room.view_one",
        "description": "View a single room",
        "category": "rooms",
    },
    # ========================================================
    # USERS
    # ========================================================
    {
        "id": 26,
        "name": "user.create",
        "description": "Create new users",
        "category": "users",
    },
    {
        "id": 27,
        "name": "user.update",
        "description": "Edit user details",
        "category": "users",
    },
    {
        "id": 28,
        "name": "user.view_one",
        "description": "View a single user",
        "category": "users",
    },
    {
        "id": 29,
        "name": "users.view_all",
        "description": "View all users",
        "category": "users",
    },
]


# ============================================================
# ALL PERMISSIONS
# ============================================================

ALL_PERMISSIONS = [permission["id"] for permission in DEFAULT_PERMISSIONS]


# ============================================================
# ROLE -> PERMISSIONS
# ============================================================

DEFAULT_ROLE_PERMISSIONS = {
    # --------------------------------------------------------
    # SUPERADMIN
    # --------------------------------------------------------
    # Superadmin receives every permission.
    ROLE_SUPERADMIN_ID: ALL_PERMISSIONS,
    # --------------------------------------------------------
    # MANAGER
    # --------------------------------------------------------
    ROLE_MANAGER_ID: [
        # Guests
        1,  # guest.create
        2,  # guest.edit
        3,  # guest.view_all
        4,  # guest_view
        # Managers
        7,  # manager.view_all
        8,  # manager.view_one
        # Reservations
        14,  # reservations.cancel
        15,  # reservations.check_in
        16,  # reservations.check_out
        17,  # reservations.confirm
        18,  # reservations.create
        19,  # reservations.edit
        20,  # reservations.view_all
        21,  # reservations.view_own
        # Rooms
        22,  # room.create
        23,  # room.update
        24,  # room.view_all
        25,  # room.view_one
        # Users
        28,  # user.view_one
        29,  # users.view_all
    ],
    # --------------------------------------------------------
    # STAFF
    # --------------------------------------------------------
    ROLE_STAFF_ID: [
        # Guests
        3,  # guest.view_all
        4,  # guest_view
        # Reservations
        14,  # reservations.cancel
        15,  # reservations.check_in
        16,  # reservations.check_out
        17,  # reservations.confirm
        18,  # reservations.create
        19,  # reservations.edit
        20,  # reservations.view_all
        21,  # reservations.view_own
        # Rooms
        24,  # room.view_all
        25,  # room.view_one
    ],
    # --------------------------------------------------------
    # GUEST
    # --------------------------------------------------------
    ROLE_GUEST_ID: [
        # Own guest profile
        2,  # guest.edit
        4,  # guest_view
        # Reservations
        14,  # reservations.cancel
        18,  # reservations.create
        21,  # reservations.view_own
        # Rooms
        24,  # room.view_all
    ],
}


# ============================================================
# DEFAULT USERS
# ============================================================
#
# IMPORTANT:
#
# SUPERADMIN is NOT stored here.
#
# The real SUPERADMIN is created from:
#
#   SUPERADMIN_NAME
#   SUPERADMIN_EMAIL
#   SUPERADMIN_PASSWORD
#   SUPERADMIN_PHONE
#
# from app.core.config.Settings.
#
# Passwords below are ONLY development/demo passwords.
# seed_all.py must hash them using hash_password()
# before saving them to the database.
# ============================================================

DEFAULT_USERS = [
    # --------------------------------------------------------
    # DEMO GUESTS
    # --------------------------------------------------------
    {
        "id": 2,
        "name": "John Kamau",
        "email": "john.kamau@example.com",
        "phone": "0712345678",
        "password": "Guest@123",
        "role_id": ROLE_GUEST_ID,
    },
    {
        "id": 3,
        "name": "Mary Wanjiku",
        "email": "mary.wanjiku@example.com",
        "phone": "0723456789",
        "password": "Guest@123",
        "role_id": ROLE_GUEST_ID,
    },
    # --------------------------------------------------------
    # DEMO MANAGERS
    # --------------------------------------------------------
    {
        "id": 4,
        "name": "David Mwangi",
        "email": "david.mwangi@grandhotel.com",
        "phone": "0734567890",
        "password": "Manager@123",
        "role_id": ROLE_MANAGER_ID,
    },
    {
        "id": 5,
        "name": "Sarah Njeri",
        "email": "sarah.njeri@grandhotel.com",
        "phone": "0745678901",
        "password": "Manager@123",
        "role_id": ROLE_MANAGER_ID,
    },
    # --------------------------------------------------------
    # DEMO STAFF
    # --------------------------------------------------------
    {
        "id": 6,
        "name": "Peter Otieno",
        "email": "peter.otieno@grandhotel.com",
        "phone": "0756789012",
        "password": "Staff@123",
        "role_id": ROLE_STAFF_ID,
    },
    {
        "id": 7,
        "name": "Grace Akinyi",
        "email": "grace.akinyi@grandhotel.com",
        "phone": "0767890123",
        "password": "Staff@123",
        "role_id": ROLE_STAFF_ID,
    },
]


# ============================================================
# DEFAULT GUESTS
# ============================================================
#
# These reference users whose role is GUEST.
#
# NOTE:
# Exact fields should match your Guests model.
# ============================================================

DEFAULT_GUESTS = [
    {
        "user_id": 2,
    },
    {
        "user_id": 3,
    },
]


# ============================================================
# DEFAULT MANAGERS
# ============================================================
#
# These reference users whose role is MANAGER.
#
# NOTE:
# Exact fields should match your Managers model.
# ============================================================

DEFAULT_MANAGERS = [
    {
        "user_id": 4,
    },
    {
        "user_id": 5,
    },
]


# ============================================================
# ROOM TYPES
# ============================================================

DEFAULT_ROOM_TYPES = [
    {
        "id": 1,
        "name": "Standard / Traditional",
        "description": (
            "The entry-level baseline. It provides everything "
            "needed for a comfortable, functional short-term stay."
        ),
        "price_per_night": 120,
        "deposit_percentage": 10,
        "amenities": (
            "Bedding: King, Queen, or Two Double beds. "
            "Bathroom: Combined shower/tub, basic towels, and "
            "standard soap/shampoo. "
            "Furniture: Work desk, one chair, nightstands, and "
            "a small wardrobe. "
            "Electronics: Flat-screen TV, bedside alarm clock, "
            "and standard Wi-Fi. "
            "Refreshments: Coffee maker, tea bags, and "
            "complimentary bottled water. "
            "Climate: In-room thermostat for heating and air "
            "conditioning. "
            "Utility: Ironing board, iron, and a small electronic "
            "room safe."
        ),
    },
    {
        "id": 2,
        "name": "Deluxe",
        "description": (
            "An upgrade in physical space, aesthetic appeal, "
            "and comfort. These rooms often feature a guaranteed "
            "better view such as a city skyline, pool, or ocean."
        ),
        "price_per_night": 185,
        "deposit_percentage": 15,
        "amenities": (
            "Space: Larger floor plan than standard rooms. "
            "Bedding: Premium mattress, higher thread-count "
            "linens, and a pillow menu. "
            "Bathroom: Upgraded vanity, rain-style showerhead, "
            "and plush bathrobes. "
            "Furniture: Added seating area, typically an armchair "
            "or a small loveseat. "
            "Electronics: Larger smart TV and high-speed premium "
            "Wi-Fi. "
            "Refreshments: Fully stocked minibar "
            "(items charged individually) and an upgraded "
            "espresso machine. "
            "Perks: Daily turndown service and a dedicated "
            "luggage rack."
        ),
    },
    {
        "id": 3,
        "name": "Superior",
        "description": (
            "Positioned physically higher in the building or in "
            "a quieter wing. It focuses on architectural advantages "
            "and enhanced luxury touches."
        ),
        "price_per_night": 275,
        "deposit_percentage": 20,
        "amenities": (
            "Location: Top floors, corner locations, or optimized "
            "architectural layouts. "
            "View: Guaranteed panoramic, unobstructed landmark "
            "or scenic views. "
            "Bathroom: Separate deep soaking tub, walk-in shower, "
            "and premium designer toiletries. "
            "Furniture: Ergonomic workstation, expansive lounge "
            "seating, and large walk-in closets. "
            "Electronics: Bluetooth room speakers, universal "
            "charging hubs, and smart room controls. "
            "Refreshments: Welcome fruit basket or local treats "
            "upon arrival. "
            "Services: Complimentary morning newspaper and free "
            "shoe-shine service."
        ),
    },
    {
        "id": 4,
        "name": "Executive / Club",
        "description": (
            "Designed for business travelers and luxury seekers. "
            "Booking this room grants exclusive access to the "
            "hotel's private VIP spaces."
        ),
        "price_per_night": 450,
        "deposit_percentage": 25,
        "amenities": (
            "Lounge Access: Free entry to the restricted "
            "Executive/Club Lounge. "
            "Lounge Food: Complimentary hot breakfast, afternoon "
            "tea, and evening hors d'oeuvres. "
            "Lounge Drinks: Free open bar featuring premium "
            "spirits, wines, and beers. "
            "Business: Free use of private lounge meeting rooms "
            "and printing services. "
            "Service: Private dedicated front desk for express "
            "check-in and check-out. "
            "Utility: Complimentary pressing of two garments "
            "per stay. "
            "Concierge: Dedicated VIP concierge handler for "
            "reservations and transport."
        ),
    },
]


# ============================================================
# DEFAULT ROOMS
# ============================================================
#
# Room prices are intentionally NOT stored here.
#
# The price comes from the RoomTypes table through:
#
#     room_type_id
#
# This prevents price duplication.
# ============================================================

DEFAULT_ROOMS = [
    {
        "id": 1,
        "room_number": 101,
        "room_type_id": 1,
        "room_availability": "reserved",
        "status": True,
        "image": "standard-101.jpg",
    },
    {
        "id": 2,
        "room_number": 102,
        "room_type_id": 1,
        "room_availability": "reserved",
        "status": True,
        "image": "standard-102.jpg",
    },
    {
        "id": 3,
        "room_number": 201,
        "room_type_id": 2,
        "room_availability": "reserved",
        "status": True,
        "image": "deluxe-201.jpg",
    },
    {
        "id": 4,
        "room_number": 202,
        "room_type_id": 2,
        "room_availability": "available",
        "status": True,
        "image": "deluxe-202.jpg",
    },
    {
        "id": 5,
        "room_number": 301,
        "room_type_id": 3,
        "room_availability": "available",
        "status": True,
        "image": "superior-301.jpg",
    },
    {
        "id": 6,
        "room_number": 302,
        "room_type_id": 3,
        "room_availability": "available",
        "status": True,
        "image": "superior-302.jpg",
    },
    {
        "id": 7,
        "room_number": 401,
        "room_type_id": 4,
        "room_availability": "available",
        "status": True,
        "image": "executive-401.jpg",
    },
    {
        "id": 8,
        "room_number": 402,
        "room_type_id": 4,
        "room_availability": "available",
        "status": True,
        "image": "executive-402.jpg",
    },
]


DEFAULT_RESERVATIONS = [

    {
        "id": 1,
        "guest_id": 1,
        "room_id": 1,

        "check_in_date": "2026-08-20T14:00:00+03:00",
        "check_out_date": "2026-08-23T11:00:00+03:00",

        "status": "confirmed",

        # Standard / Traditional
        "room_price_per_night": 120,
        "deposit_percentage": 10,

        # 120 × 3 nights = 360
        # 10% of 360 = 36
        "deposit_amount": 36,
    },

    {
        "id": 2,
        "guest_id": 2,
        "room_id": 2,

        "check_in_date": "2026-08-22T14:00:00+03:00",
        "check_out_date": "2026-08-25T11:00:00+03:00",

        "status": "confirmed",

        # Deluxe
        "room_price_per_night": 185,
        "deposit_percentage": 15,

        # 185 × 3 = 555
        # 15% = 83.25
        #
        # Since your column is Integer, decide whether
        # you want to round this to 83 or change the
        # monetary columns to Numeric.
        "deposit_amount": 83,
    },

    {
        "id": 3,
        "guest_id": 2,
        "room_id": 3,

        "check_in_date": "2026-08-26T14:00:00+03:00",
        "check_out_date": "2026-08-29T11:00:00+03:00",

        "status": "pending",

        # Superior
        "room_price_per_night": 275,
        "deposit_percentage": 20,

        # 275 × 3 = 825
        # 20% = 165
        "deposit_amount": 165,
    },

    {
        "id": 4,
        "guest_id": 1,
        "room_id": 4,

        "check_in_date": "2026-09-01T14:00:00+03:00",
        "check_out_date": "2026-09-05T11:00:00+03:00",

        "status": "cancelled",

        # Executive / Club
        "room_price_per_night": 450,
        "deposit_percentage": 25,

        # 450 × 4 = 1800
        # 25% = 450
        "deposit_amount": 450,
    },
]
DEFAULT_PAYMENTS = [

    # --------------------------------------------------------
    # Reservation 1
    # M-Pesa payment
    # --------------------------------------------------------

    {
        "id": 1,
        "reservation_id": 1,
        "amount": 360,
        "payment_type":"deposit",
        "payment_method": "mpesa",

        "transaction_reference": "DEMO-MPESA-001",
        "payment_reference": "DEMO-MPESA-RECEIPT-001",

        "status": "paid",
    },

    # --------------------------------------------------------
    # Reservation 2
    # Card / Flutterwave payment
    # --------------------------------------------------------

    {
        "id": 2,
        "reservation_id": 2,
        "amount": 555,
        "payment_type":"deposit",
        "payment_method": "card",

        "transaction_reference": "DEMO-CARD-001",
        "payment_reference": "DEMO-FLW-001",

        "status": "paid",
    },

    # --------------------------------------------------------
    # Reservation 3
    # M-Pesa payment still pending
    # --------------------------------------------------------

    {
        "id": 3,
        "reservation_id": 3,
        "amount": 550,
        "payment_type":"deposit",
        "payment_method": "mpesa",

        "transaction_reference": "DEMO-MPESA-002",
        "payment_reference": None,

        "status": "pending",
    },

    # --------------------------------------------------------
    # Reservation 4
    # Card payment failed
    # --------------------------------------------------------

    {
        "id": 4,
        "reservation_id": 4,
        "amount": 740,
        "payment_type":"deposit",
        "payment_method": "card",

        "transaction_reference": "DEMO-CARD-002",
        "payment_reference": None,

        "status": "failed",
    },
]