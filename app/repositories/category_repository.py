from __future__ import annotations

from typing import List, Protocol
from app.models.category import Category


class CategoryRepository(Protocol):
    def list_ordered(self) -> List[Category]:
        ...

    def get(self, category_id: int) -> Category:
        ...

    def add(self, category: Category) -> None:
        ...

    def commit(self) -> None:
        ...

    def delete(self, category: Category) -> None:
        ...