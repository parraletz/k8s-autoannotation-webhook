"""In memory repository for items"""

from typing import Dict, List, Optional

from app.domain.models import Item, ItemId


class InMemoryRepository:
    """
    In memory repository for items
    """

    def __init__(self) -> None:
        """
        Initialize the repository
        """
        self.data: Dict[ItemId, Item] = {}

    def save(self, item: Item) -> None:
        """
        Save an item
        """
        self.data[item.id] = item

    def get(self, id: ItemId) -> Optional[Item]:
        """
        Get an item by id
        """
        return self.data.get(id)

    def delete(self, id: ItemId) -> bool:
        """
        Delete an item by id
        """
        return self.data.pop(id, None) is not None

    def list_all(self) -> List[Item]:
        """
        List all items
        """
        return list(self.data.values())

    def update(self, item: Item) -> None:
        """
        Update an item
        """
        self.data[item.id] = item
