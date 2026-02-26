from app import db

# New category
class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)

    # Handle join
    password_entries = db.relationship(
        "PasswordEntry",
        secondary="password_entry_categories",
        back_populates="categories",
        lazy=True,
    )
