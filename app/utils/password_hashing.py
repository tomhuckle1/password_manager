from __future__ import annotations

from typing import Protocol
from flask_bcrypt import Bcrypt


class PasswordHasher(Protocol):
    def hash(self, plain: str) -> str:
        ...

    def verify(self, hashed: str, plain: str) -> bool:
        ...


class BcryptPasswordHasher(PasswordHasher):
    def __init__(self, bcrypt: Bcrypt):
        self.bcrypt = bcrypt

    def hash(self, plain: str) -> str:
        return self.bcrypt.generate_password_hash(plain).decode("utf-8")

    def verify(self, hashed: str, plain: str) -> bool:
        return self.bcrypt.check_password_hash(hashed, plain)