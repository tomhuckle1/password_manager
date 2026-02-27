from __future__ import annotations
from flask_migrate import upgrade
from app import create_app, db, bcrypt
from app.models import User, Category, PasswordEntry
from app.models.user import ROLE_ADMIN, ROLE_REGULAR
from app.utils.encryptor import FernetEncryptor


def reset_database() -> None:
    # Bring up to date
    upgrade()

    # Clear tables
    db.session.execute(db.text("DELETE FROM password_entry_categories"))
    db.session.execute(db.text("DELETE FROM password_entries"))
    db.session.execute(db.text("DELETE FROM categories"))
    db.session.execute(db.text("DELETE FROM users"))
    db.session.commit()


def hash_pw(pw: str) -> str:
    return bcrypt.generate_password_hash(pw).decode("utf-8")


def main() -> None:
    app = create_app()

    with app.app_context():
        reset_database()

        encryptor = FernetEncryptor(app.config["ENCRYPTION_KEY"])

        # Users
        admin = User(
            name="Admin User",
            email="admin@example.com",
            password_hash=hash_pw("AdminPass123!"),
            role=ROLE_ADMIN,
        )
        regular = User(
            name="Regular User",
            email="user@example.com",
            password_hash=hash_pw("Password123!"),
            role=ROLE_REGULAR,
        )

        db.session.add_all([admin, regular])
        db.session.commit()

        # Categories
        categories = [
            Category(name="Banking", description="Online banking"),
            Category(name="Government", description="UK government services"),
            Category(name="Utilities", description="Energy, water and telecom providers"),
            Category(name="Insurance", description="Insurance providers"),
            Category(name="Property", description="Property management"),
            Category(name="Transport", description="transport systems"),
        ]
        db.session.add_all(categories)
        db.session.commit()

        cat = {c.name: c for c in categories}

        # Passwords
        entries_data = [
            ("Barclays Business Banking", "https://bank.barclays.co.uk", "biz-admin", "Barclays!123", "Account access.", ["Banking"]),
            ("HMRC Business Tax Account", "https://www.gov.uk/log-in-register-hmrc-online-services", "hmrc-user", "TaxPwd!123", "VAT submissions.", ["Government"]),
            ("Companies House WebFiling", "https://ewf.companieshouse.gov.uk", "ch-admin", "ChPwd!123", "Company config.", ["Government"]),
            ("British Gas Business", "https://www.britishgas.co.uk/business", "energy-admin", "EnergyPwd!123", "Gas management.", ["Utilities"]),
            ("Thames Water Portal", "https://www.thameswater.co.uk/business", "water-user", "WaterPwd!123", "water services.", ["Utilities"]),
            ("Aviva Business Insurance", "https://www.aviva.co.uk/business", "insurance-user", "Insure!123", "Policy documents and claims.", ["Insurance"]),
            ("Rightmove Landlord Account", "https://www.rightmove.co.uk", "landlord-user", "Property!123", "Rental listings.", ["Property"]),
            ("Zoopla Property Manager", "https://www.zoopla.co.uk", "zoopla-admin", "Zoopla!123", "Property portfolio management.", ["Property"]),
            ("National Rail Business", "https://www.nationalrail.co.uk", "travel-admin", "RailPwd!123", "Rail bookings.", ["Transport"]),
            ("TfL Oyster Admin", "https://tfl.gov.uk", "tfl-admin", "Oyster!123", "Transport for London.", ["Transport"]),
        ]

        entries: list[PasswordEntry] = []
        for name, website, username, plain_pw, notes, category_names in entries_data:
            entry = PasswordEntry(
                name=name,
                website=website,
                account_username=username,
                password_value=encryptor.encrypt(plain_pw),
                notes=notes,
                created_by_user_id=admin.id,
                updated_by_user_id=admin.id,
            )
            entry.categories = [cat[n] for n in category_names]
            entries.append(entry)

        db.session.add_all(entries)
        db.session.commit()


if __name__ == "__main__":
    main()