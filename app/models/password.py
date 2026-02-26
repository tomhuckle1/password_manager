from app import db

# Join table
password_entry_categories = db.Table(
    "password_entry_categories",
    db.Column(
        "password_entry_id",
        db.Integer,
        db.ForeignKey("password_entries.id"),
        primary_key=True,
    ),
    db.Column(
        "category_id",
        db.Integer,
        db.ForeignKey("categories.id"),
        primary_key=True,
    ),
)

# Index
db.Index("ix_pwcat_password_entry_id", password_entry_categories.c.password_entry_id)
db.Index("ix_pwcat_category_id", password_entry_categories.c.category_id)

# New Password
class PasswordEntry(db.Model):
    __tablename__ = "password_entries"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(200), nullable=False)
    account_username = db.Column(db.String(120), nullable=False)

    password_value = db.Column(db.String(500), nullable=False)
    notes = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=db.func.now(), nullable=True)

    # Handle join
    categories = db.relationship(
        "Category",
        secondary=password_entry_categories,
        back_populates="password_entries",
        lazy=True,
    )

    created_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    updated_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)

    # User relationship
    created_by = db.relationship("User", foreign_keys=[created_by_user_id])
    updated_by = db.relationship("User", foreign_keys=[updated_by_user_id])
