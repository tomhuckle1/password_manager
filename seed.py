from __future__ import annotations
from flask_migrate import upgrade
from app import create_app, db, bcrypt
from app.models import User, Category, PasswordEntry
from app.models.user import ROLE_ADMIN, ROLE_REGULAR
from app.utils.encryptor import FernetEncryptor

def hash_pw(pw: str) -> str:
    return bcrypt.generate_password_hash(pw).decode("utf-8")

def reset_database() -> None:
    # Apply any pending migrations to the database
    upgrade()

    # Clear tables to ensure a clean slate
    db.session.execute(db.text("DELETE FROM password_entry_categories"))
    db.session.execute(db.text("DELETE FROM password_entries"))
    db.session.execute(db.text("DELETE FROM categories"))
    db.session.execute(db.text("DELETE FROM users"))
    db.session.commit()

def main() -> None:
    app = create_app()

    with app.app_context():
        # Reset the database to ensure the latest migrations are applied
        reset_database()

        encryptor = FernetEncryptor(app.config["ENCRYPTION_KEY"])

        # Users
        admin = User.query.filter_by(email="admin@example.com").first()
        if not admin:
            admin = User(
                name="Admin User",
                email="admin@example.com",
                password_hash=hash_pw("AdminPass123!"),
                role=ROLE_ADMIN,
            )
            db.session.add(admin)

        regular = User.query.filter_by(email="user@example.com").first()
        if not regular:
            regular = User(
                name="Regular User",
                email="user@example.com",
                password_hash=hash_pw("Password123!"),
                role=ROLE_REGULAR,
            )
            db.session.add(regular)

        db.session.commit()

        # Categories
        categories_data = [
            ("Banking", "Online banking"),
            ("Government", "UK government services"),
            ("Utilities", "Energy, water and telecom providers"),
            ("Insurance", "Insurance providers"),
            ("Property", "Property management"),
            ("Transport", "Transport systems"),
        ]

        categories = []
        for name, desc in categories_data:
            cat = Category.query.filter_by(name=name).first()
            if not cat:
                cat = Category(name=name, description=desc)
                db.session.add(cat)
            categories.append(cat)

        db.session.commit()

        cat = {c.name: c for c in categories}

        # Passwords
        entries_data = [
            ("Barclays Business Banking", "bank.barclays.co.uk", "biz-admin", "Barclays!123", "Account access.", ["Banking"]),
            ("HMRC Business Tax Account", "gov.uk", "hmrc-user", "TaxPwd!123", "VAT submissions.", ["Government"]),
            ("Companies House WebFiling", "ewf.companieshouse.gov.uk", "ch-admin", "ChPwd!123", "Company config.", ["Government"]),
            ("British Gas Business", "www.britishgas.co.uk", "energy-admin", "EnergyPwd!123", "Gas management.", ["Utilities"]),
            ("Thames Water Portal", "thameswater.co.uk", "water-user", "WaterPwd!123", "Water services.", ["Utilities"]),
            ("Aviva Business Insurance", "aviva.co.uk", "insurance-user", "Insure!123", "Policy documents and claims.", ["Insurance"]),
            ("Rightmove Landlord Account", "www.rightmove.co.uk", "landlord-user", "Property!123", "Rental listings.", ["Property"]),
            ("Zoopla Property Manager", "zoopla.co.uk", "zoopla-admin", "Zoopla!123", "Property portfolio management.", ["Property"]),
            ("National Rail Business", "nationalrail.co.uk", "travel-admin", "RailPwd!123", "Rail bookings.", ["Transport"]),
            ("TfL Oyster Admin", "tfl.gov.uk", "tfl-admin", "Oyster!123", "Transport for London.", ["Transport"]),
        ]

        entries = []
        for name, website, username, plain_pw, notes, category_names in entries_data:
            entry = PasswordEntry.query.filter_by(website=website, account_username=username).first()
            if not entry:
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
                db.session.add(entry)

        db.session.commit()

if __name__ == "__main__":
    main()