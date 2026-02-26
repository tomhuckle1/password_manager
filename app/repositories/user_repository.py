from __future__ import annotations
from typing import Optional, Protocol
from app.models.user import User


class UserRepository(Protocol):
    def get_by_email(self, email: str) -> Optional[User]:
        ...

    def get_by_id(self, user_id: int) -> Optional[User]:
        ...

    def add(self, user: User) -> None:
        ...