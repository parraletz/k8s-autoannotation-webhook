"""
Domain ports
"""

from typing import Iterable, Optional, Protocol

from .models import Item, ItemId


class ItemRepository(Protocol):
    """
    Item repository interface
    """

    def save(self, item: Item) -> None: ...
    def get(self, id: ItemId) -> Optional[Item]: ...
    def list_all(self) -> Iterable[Item]: ...
    def delete(self, id: ItemId) -> bool: ...
    def update(self, item: Item) -> None: ...
