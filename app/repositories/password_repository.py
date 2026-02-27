from __future__ import annotations

from typing import Protocol
from app.models.password import PasswordEntry


class PasswordRepository(Protocol):
    def get_or_404(self, entry_id: int) -> PasswordEntry:
        ...

    def add(self, entry: PasswordEntry) -> None:
        ...

    def commit(self) -> None:
        ...

    def delete(self, entry: PasswordEntry) -> None:
        ...