from flask_login import UserMixin
from app import db, login_manager


# User roles
ROLE_ADMIN = "admin"
ROLE_REGULAR = "regular"


# Keep logged in
@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "users" 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=ROLE_REGULAR)

    # Constraint to ensure role is either admin or regular
    __table_args__ = (
        db.CheckConstraint(
            f"role IN ('{ROLE_ADMIN}','{ROLE_REGULAR}')",
            name="ck_user_role"
        ),
    )

    # Helper to check if the user is admin
    def is_admin(self) -> bool:
        return self.role == ROLE_ADMIN