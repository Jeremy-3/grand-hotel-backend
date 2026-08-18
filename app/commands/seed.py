"""
Grand Hotel - FastAPI Database Seeder

Run with:

    python -m app.commands.seed_all

Seeds:

    - Roles
    - Permissions
    - Role/Permission mappings
    - Users
    - Managers
    - Guests
    - Room Types
    - Rooms

Reservations and Payments are NOT seeded because they should
be created through the actual hotel booking/payment system.
"""

from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.core.security import hash_password

from app.core.constants import (
    DEFAULT_ROLES,
    DEFAULT_PERMISSIONS,
    DEFAULT_ROLE_PERMISSIONS,
    DEFAULT_USERS,
    DEFAULT_MANAGERS,
    DEFAULT_GUESTS,
    DEFAULT_ROOM_TYPES,
    DEFAULT_ROOMS,
    ROLE_SUPERADMIN_ID,
)

from app.db.base import Base
from app.db.local_connector import engine
from app.db.utils import db_context
from app.models.roles import Roles
from app.models.permissions import Permissions
from app.models.role_permissions import RolePermission
from app.models.users import Users
from app.models.manager import Managers
from app.models.guests import Guests
from app.models.room_types import RoomTypes
from app.models.rooms import Rooms


# ============================================================
# GENERIC SEED FUNCTION
# ============================================================

def seed_table(
    db,
    model,
    data,
    table_name: str,
    flush: bool = False,
):
    """
    Insert records into a table.

    If a row contains an ID and that ID already exists,
    the row is skipped.
    """

    print(f"Seeding {table_name}...")

    created = 0

    for row in data:

        # ----------------------------------------------------
        # Check existing record by primary key
        # ----------------------------------------------------

        pk = row.get("id")

        if pk is not None and db.get(model, pk):
            continue

        # ----------------------------------------------------
        # Create model instance
        # ----------------------------------------------------

        obj = model(**row)

        db.add(obj)

        created += 1

    if flush:
        db.flush()

    db.commit()

    print(f"✓ Inserted {created} {table_name}")


# ============================================================
# ROLE PERMISSIONS
# ============================================================

def seed_role_permissions(db):
    """
    Create role-permission relationships.
    """

    print("Seeding role-permission mappings...")

    created = 0

    for role_id, permission_ids in DEFAULT_ROLE_PERMISSIONS.items():

        for permission_id in permission_ids:

            exists = (
                db.query(RolePermission)
                .filter_by(
                    role_id=role_id,
                    permission_id=permission_id,
                )
                .first()
            )

            if exists:
                continue

            db.add(
                RolePermission(
                    role_id=role_id,
                    permission_id=permission_id,
                )
            )

            created += 1

    db.commit()

    print(
        f"✓ Created {created} role-permission mappings"
    )


# ============================================================
# SUPERADMIN
# ============================================================

def seed_superadmin(db):
    """
    Create the Grand Hotel SUPERADMIN from environment
    variables.

    Required settings:

        SUPERADMIN_NAME
        SUPERADMIN_EMAIL
        SUPERADMIN_PHONE
        SUPERADMIN_PASSWORD
    """

    print("Checking SUPERADMIN...")

    if not settings.SUPERADMIN_EMAIL:

        print(
            "⚠️ SUPERADMIN_EMAIL not set, "
            "skipping SUPERADMIN creation"
        )

        return

    # --------------------------------------------------------
    # Check existing user
    # --------------------------------------------------------

    exists = (
        db.query(Users)
        .filter(
            Users.email == settings.SUPERADMIN_EMAIL
        )
        .first()
    )

    if exists:

        print(
            "✅ SUPERADMIN already exists, skipping"
        )

        return

    # --------------------------------------------------------
    # Create SUPERADMIN
    # --------------------------------------------------------

    user = Users(
        name=settings.SUPERADMIN_NAME,
        email=settings.SUPERADMIN_EMAIL,
        phone_number=settings.SUPERADMIN_PHONE,
        password_hash=hash_password(
            settings.SUPERADMIN_PASSWORD
        ),
        is_active=True,
        role_id=ROLE_SUPERADMIN_ID,
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    print(
        f"✓ SUPERADMIN created: "
        f"{settings.SUPERADMIN_EMAIL}"
    )


# ============================================================
# MANAGERS
# ============================================================

def seed_managers(db):
    """
    Seed manager records.

    Managers reference Users through user_id, therefore Users
    must exist before Managers are inserted.
    """

    print("Seeding managers...")

    created = 0

    for row in DEFAULT_MANAGERS:

        user_id = row.get("user_id")

        # ----------------------------------------------------
        # Check existing manager
        # ----------------------------------------------------

        exists = (
            db.query(Managers)
            .filter(
                Managers.user_id == user_id
            )
            .first()
        )

        if exists:
            continue

        manager = Managers(**row)

        db.add(manager)

        created += 1

    db.commit()

    print(
        f"✓ Inserted {created} managers"
    )


# ============================================================
# GUESTS
# ============================================================

def seed_guests(db):
    """
    Seed guest profiles.

    Guests reference Users through user_id.
    """

    print("Seeding guests...")

    created = 0

    for row in DEFAULT_GUESTS:

        user_id = row.get("user_id")

        exists = (
            db.query(Guests)
            .filter(
                Guests.user_id == user_id
            )
            .first()
        )

        if exists:
            continue

        guest = Guests(**row)

        db.add(guest)

        created += 1

    db.commit()

    print(
        f"✓ Inserted {created} guests"
    )


# ============================================================
# MAIN SEED
# ============================================================

def seed_all():

    print("\n" + "=" * 60)
    print("GRAND HOTEL DATABASE SEEDING")
    print("=" * 60 + "\n")

    # --------------------------------------------------------
    # Database check
    # --------------------------------------------------------

    if not settings.DATABASE_URL:

        print(
            "❌ DATABASE_URL not set, "
            "skipping all seeding"
        )

        return

    # --------------------------------------------------------
    # Create database tables
    # --------------------------------------------------------

    Base.metadata.create_all(bind=engine)

    print("✓ Tables created")

    # --------------------------------------------------------
    # Database session
    # --------------------------------------------------------

    with db_context() as db:

        try:

            # =================================================
            # RBAC
            # =================================================

            print("\n" + "-" * 60)
            print("RBAC")
            print("-" * 60)

            seed_table(
                db,
                Roles,
                DEFAULT_ROLES,
                "roles",
            )

            seed_table(
                db,
                Permissions,
                DEFAULT_PERMISSIONS,
                "permissions",
            )

            seed_role_permissions(db)

            # =================================================
            # SUPERADMIN
            # =================================================

            print("\n" + "-" * 60)
            print("SUPERADMIN")
            print("-" * 60)

            seed_superadmin(db)

            # =================================================
            # USERS
            # =================================================

            print("\n" + "-" * 60)
            print("USERS")
            print("-" * 60)

            seed_table(
                db,
                Users,
                DEFAULT_USERS,
                "users",
            )

            # =================================================
            # MANAGERS
            # =================================================

            print("\n" + "-" * 60)
            print("MANAGERS")
            print("-" * 60)

            seed_managers(db)

            # =================================================
            # GUESTS
            # =================================================

            print("\n" + "-" * 60)
            print("GUESTS")
            print("-" * 60)

            seed_guests(db)

            # =================================================
            # ROOM TYPES
            # =================================================

            print("\n" + "-" * 60)
            print("ROOM TYPES")
            print("-" * 60)

            seed_table(
                db,
                RoomTypes,
                DEFAULT_ROOM_TYPES,
                "room types",
                flush=True,
            )

            # =================================================
            # ROOMS
            # =================================================

            print("\n" + "-" * 60)
            print("ROOMS")
            print("-" * 60)

            seed_table(
                db,
                Rooms,
                DEFAULT_ROOMS,
                "rooms",
            )

            # =================================================
            # RESERVATIONS
            # =================================================

            print("\n" + "-" * 60)
            print("RESERVATIONS")
            print("-" * 60)

            print(
                "ℹ️ Reservations are not seeded."
            )

            print(
                "   Reservations should be created "
                "through the booking system."
            )

            # =================================================
            # PAYMENTS
            # =================================================

            print("\n" + "-" * 60)
            print("PAYMENTS")
            print("-" * 60)

            print(
                "ℹ️ Payments are not seeded."
            )

            print(
                "   Payments should be created when "
                "a reservation is made."
            )

            # =================================================
            # COMPLETE
            # =================================================

            print("\n" + "=" * 60)
            print(
                "✓ GRAND HOTEL DATABASE SEEDING "
                "COMPLETED SUCCESSFULLY"
            )
            print("=" * 60 + "\n")

        except IntegrityError as e:

            db.rollback()

            print(
                "✗ Integrity error during seeding"
            )

            raise e

        except Exception as e:

            db.rollback()

            print(
                f"✗ Seeding failed: {str(e)}"
            )

            raise


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    seed_all()

