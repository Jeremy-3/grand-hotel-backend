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
    # USERS
    # ========================================================
    {
        "id": 1,
        "name": "users.view_all",
        "description": "View all users",
        "category": "users",
    },
    {
        "id": 2,
        "name": "users.create",
        "description": "Create new users",
        "category": "users",
    },
    {
        "id": 3,
        "name": "users.edit",
        "description": "Edit user details",
        "category": "users",
    },
    {
        "id": 4,
        "name": "users.delete",
        "description": "Delete users",
        "category": "users",
    },
    {
        "id": 5,
        "name": "users.view_own",
        "description": "View own profile",
        "category": "users",
    },
    {
        "id": 6,
        "name": "users.edit_own",
        "description": "Edit own profile",
        "category": "users",
    },
    # ========================================================
    # ROLES & PERMISSIONS
    # ========================================================
    {"id": 7, "name": "roles.view", "description": "View roles", "category": "roles"},
    {
        "id": 8,
        "name": "roles.create",
        "description": "Create roles",
        "category": "roles",
    },
    {"id": 9, "name": "roles.edit", "description": "Edit roles", "category": "roles"},
    {
        "id": 10,
        "name": "roles.delete",
        "description": "Delete roles",
        "category": "roles",
    },
    {
        "id": 11,
        "name": "permissions.manage",
        "description": "Manage permissions",
        "category": "roles",
    },
    # ========================================================
    # GUESTS
    # ========================================================
    {
        "id": 12,
        "name": "guests.view_all",
        "description": "View all guests",
        "category": "guests",
    },
    {
        "id": 13,
        "name": "guests.create",
        "description": "Create guest profiles",
        "category": "guests",
    },
    {
        "id": 14,
        "name": "guests.edit",
        "description": "Edit guest details",
        "category": "guests",
    },
    {
        "id": 15,
        "name": "guests.delete",
        "description": "Delete guest profiles",
        "category": "guests",
    },
    {
        "id": 16,
        "name": "guests.view_own",
        "description": "View own guest profile",
        "category": "guests",
    },
    {
        "id": 17,
        "name": "guests.edit_own",
        "description": "Edit own guest profile",
        "category": "guests",
    },
    # ========================================================
    # ROOM TYPES
    # ========================================================
    {
        "id": 18,
        "name": "room_types.view",
        "description": "View room types",
        "category": "room_types",
    },
    {
        "id": 19,
        "name": "room_types.create",
        "description": "Create room types",
        "category": "room_types",
    },
    {
        "id": 20,
        "name": "room_types.edit",
        "description": "Edit room types",
        "category": "room_types",
    },
    {
        "id": 21,
        "name": "room_types.delete",
        "description": "Delete room types",
        "category": "room_types",
    },
    # ========================================================
    # ROOMS
    # ========================================================
    {
        "id": 22,
        "name": "rooms.view_all",
        "description": "View all rooms",
        "category": "rooms",
    },
    {
        "id": 23,
        "name": "rooms.view_available",
        "description": "View available rooms",
        "category": "rooms",
    },
    {
        "id": 24,
        "name": "rooms.create",
        "description": "Create rooms",
        "category": "rooms",
    },
    {
        "id": 25,
        "name": "rooms.edit",
        "description": "Edit room details",
        "category": "rooms",
    },
    {
        "id": 26,
        "name": "rooms.delete",
        "description": "Delete rooms",
        "category": "rooms",
    },
    {
        "id": 27,
        "name": "rooms.update_status",
        "description": "Update room status",
        "category": "rooms",
    },
    # ========================================================
    # RESERVATIONS
    # ========================================================
    {
        "id": 28,
        "name": "reservations.view_all",
        "description": "View all reservations",
        "category": "reservations",
    },
    {
        "id": 29,
        "name": "reservations.view_own",
        "description": "View own reservations",
        "category": "reservations",
    },
    {
        "id": 30,
        "name": "reservations.create",
        "description": "Create reservations",
        "category": "reservations",
    },
    {
        "id": 31,
        "name": "reservations.edit",
        "description": "Edit reservation details",
        "category": "reservations",
    },
    {
        "id": 32,
        "name": "reservations.cancel",
        "description": "Cancel reservations",
        "category": "reservations",
    },
    {
        "id": 33,
        "name": "reservations.confirm",
        "description": "Confirm reservations",
        "category": "reservations",
    },
    {
        "id": 34,
        "name": "reservations.check_in",
        "description": "Check guests in",
        "category": "reservations",
    },
    {
        "id": 35,
        "name": "reservations.check_out",
        "description": "Check guests out",
        "category": "reservations",
    },
    {
        "id": 36,
        "name": "reservations.view_history",
        "description": "View reservation history",
        "category": "reservations",
    },
    # ========================================================
    # DEPOSITS
    # ========================================================
    {
        "id": 37,
        "name": "deposits.view_all",
        "description": "View all deposits",
        "category": "deposits",
    },
    {
        "id": 38,
        "name": "deposits.view_own",
        "description": "View own deposits",
        "category": "deposits",
    },
    {
        "id": 39,
        "name": "deposits.create",
        "description": "Create deposit records",
        "category": "deposits",
    },
    {
        "id": 40,
        "name": "deposits.confirm",
        "description": "Confirm deposit payments",
        "category": "deposits",
    },
    {
        "id": 41,
        "name": "deposits.refund",
        "description": "Refund deposits",
        "category": "deposits",
    },
    # ========================================================
    # PAYMENTS
    # ========================================================
    {
        "id": 42,
        "name": "payments.view_all",
        "description": "View all payments",
        "category": "payments",
    },
    {
        "id": 43,
        "name": "payments.view_own",
        "description": "View own payments",
        "category": "payments",
    },
    {
        "id": 44,
        "name": "payments.process",
        "description": "Process payments",
        "category": "payments",
    },
    {
        "id": 45,
        "name": "payments.verify",
        "description": "Verify payment transactions",
        "category": "payments",
    },
    {
        "id": 46,
        "name": "payments.refund",
        "description": "Process payment refunds",
        "category": "payments",
    },
    {
        "id": 47,
        "name": "payments.view_details",
        "description": "View payment details",
        "category": "payments",
    },
    # ========================================================
    # MANAGERS
    # ========================================================
    {
        "id": 48,
        "name": "managers.view_all",
        "description": "View all managers",
        "category": "managers",
    },
    {
        "id": 49,
        "name": "managers.create",
        "description": "Create manager accounts",
        "category": "managers",
    },
    {
        "id": 50,
        "name": "managers.edit",
        "description": "Edit manager details",
        "category": "managers",
    },
    {
        "id": 51,
        "name": "managers.delete",
        "description": "Delete managers",
        "category": "managers",
    },
    # ========================================================
    # STAFF
    # ========================================================
    {
        "id": 52,
        "name": "staff.view_all",
        "description": "View all staff",
        "category": "staff",
    },
    {
        "id": 53,
        "name": "staff.create",
        "description": "Create staff accounts",
        "category": "staff",
    },
    {
        "id": 54,
        "name": "staff.edit",
        "description": "Edit staff details",
        "category": "staff",
    },
    {
        "id": 55,
        "name": "staff.delete",
        "description": "Delete staff",
        "category": "staff",
    },
    # ========================================================
    # DASHBOARD
    # ========================================================
    {
        "id": 56,
        "name": "dashboard.admin",
        "description": "Access administrator dashboard",
        "category": "dashboard",
    },
    {
        "id": 57,
        "name": "dashboard.manager",
        "description": "Access manager dashboard",
        "category": "dashboard",
    },
    {
        "id": 58,
        "name": "dashboard.staff",
        "description": "Access staff dashboard",
        "category": "dashboard",
    },
    {
        "id": 59,
        "name": "dashboard.guest",
        "description": "Access guest dashboard",
        "category": "dashboard",
    },
    # ========================================================
    # REPORTS & ANALYTICS
    # ========================================================
    {
        "id": 60,
        "name": "analytics.view",
        "description": "View analytics dashboard",
        "category": "analytics",
    },
    {
        "id": 61,
        "name": "analytics.export",
        "description": "Export analytics data",
        "category": "analytics",
    },
    {
        "id": 62,
        "name": "reports.reservations",
        "description": "View reservation reports",
        "category": "analytics",
    },
    {
        "id": 63,
        "name": "reports.payments",
        "description": "View payment reports",
        "category": "analytics",
    },
    {
        "id": 64,
        "name": "reports.guests",
        "description": "View guest reports",
        "category": "analytics",
    },
    {
        "id": 65,
        "name": "reports.occupancy",
        "description": "View room occupancy reports",
        "category": "analytics",
    },
    {
        "id": 66,
        "name": "reports.revenue",
        "description": "View revenue reports",
        "category": "analytics",
    },
    # ========================================================
    # PROFILE
    # ========================================================
    {
        "id": 67,
        "name": "profile.view",
        "description": "View own profile",
        "category": "profile",
    },
    {
        "id": 68,
        "name": "profile.edit",
        "description": "Edit own profile",
        "category": "profile",
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
        # Users
        1,
        2,
        3,
        4,
        # Guests
        5,
        6,
        7,
        8,
        # Rooms
        9,
        10,
        11,
        12,
        # Room Types
        13,
        14,
        15,
        16,
        # Reservations
        17,
        18,
        19,
        20,
        # Payments
        21,
        22,
        23,
        # Managers
        24,
        25,
        26,
        27,
        # Staff
        28,
        29,
        30,
        31,
    ],
    # --------------------------------------------------------
    # STAFF
    # --------------------------------------------------------
    ROLE_STAFF_ID: [
        # Guests
        5,
        6,
        7,
        # Rooms
        10,
        # Room Types
        14,
        # Reservations
        17,
        18,
        19,
        20,
        # Payments
        21,
        22,
        # Staff
        29,
    ],
    # --------------------------------------------------------
    # GUEST
    # --------------------------------------------------------
    ROLE_GUEST_ID: [
        # Own/basic guest functionality
        6,
        7,
        # View rooms
        10,
        # View room types
        14,
        # Reservations
        17,
        18,
        19,
        20,
        # Payments
        21,
        22,
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
        "availability": True,
        "status": "available",
        "image": "standard-101.jpg",
        "amenities": None,
    },
    {
        "id": 2,
        "room_number": 102,
        "room_type_id": 1,
        "availability": True,
        "status": "available",
        "image": "standard-102.jpg",
        "amenities": None,
    },
    {
        "id": 3,
        "room_number": 201,
        "room_type_id": 2,
        "availability": True,
        "status": "available",
        "image": "deluxe-201.jpg",
        "amenities": None,
    },
    {
        "id": 4,
        "room_number": 202,
        "room_type_id": 2,
        "availability": True,
        "status": "available",
        "image": "deluxe-202.jpg",
        "amenities": None,
    },
    {
        "id": 5,
        "room_number": 301,
        "room_type_id": 3,
        "availability": True,
        "status": "available",
        "image": "superior-301.jpg",
        "amenities": None,
    },
    {
        "id": 6,
        "room_number": 302,
        "room_type_id": 3,
        "availability": True,
        "status": "available",
        "image": "superior-302.jpg",
        "amenities": None,
    },
    {
        "id": 7,
        "room_number": 401,
        "room_type_id": 4,
        "availability": True,
        "status": "available",
        "image": "executive-401.jpg",
        "amenities": None,
    },
    {
        "id": 8,
        "room_number": 402,
        "room_type_id": 4,
        "availability": True,
        "status": "available",
        "image": "executive-402.jpg",
        "amenities": None,
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
        "guest_id": 3,
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
        "guest_id": 4,
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
        "payment_method": "card",

        "transaction_reference": "DEMO-CARD-002",
        "payment_reference": None,

        "status": "failed",
    },
]
