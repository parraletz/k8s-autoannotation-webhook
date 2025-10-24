"""Handlers for item domain"""

from datetime import datetime
from typing import List, Optional

from app.domain.errors import NotFoundError
from app.domain.interfaces import ItemRepository
from app.domain.models import Item, ItemId
from app.tools.validator import require


class AddItem:
    """Add item handler"""

    def __init__(self, repository: ItemRepository) -> None:
        self.repository = repository

    def execute(self, id: str, name: str, description: str, price: float) -> Item:
        require(id.strip() != "", "Id cannot be empty")
        now = datetime.now()
        item = Item(
            ItemId(int(id)),
            name.strip(),
            description.strip(),
            float(price),
            created_at=now,
            updated_at=now,
        )
        item.validate()
        self.repository.save(item)
        return item


class GetItem:
    """Get item handler"""

    def __init__(self, repository: ItemRepository) -> None:
        self.repository = repository

    def execute(self, id: ItemId) -> Item:
        item = self.repository.get(id)
        if not item:
            raise NotFoundError("Item not found")
        return item


class DeleteItem:
    """Delete Item handler"""

    def __init__(self, repository: ItemRepository) -> None:
        self.repository = repository

    def execute(self, id: ItemId) -> None:
        ok = self.repository.delete(id)
        if not ok:
            raise NotFoundError("Item not found")


class ListItems:
    """List items handler"""

    def __init__(self, repository: ItemRepository) -> None:
        self.repository = repository

    def execute(self) -> List[Item]:
        return self.repository.list_all()  # return sorted(self.repository.list_all(), key=lambda item: item.name.lower())


class UpdateItem:
    """Update item handler"""

    def __init__(self, repository: ItemRepository) -> None:
        self.repository = repository

    def execute(self, id: ItemId, name: Optional[str] = None, description: Optional[str] = None, price: Optional[float] = None) -> Item:
        existing = self.repository.get(id)
        if not existing:
            raise NotFoundError("Item not found")
        updated = Item(
            id=existing.id,
            name=name.strip() if name else existing.name,
            price=float(price) if price is not None else existing.price,
            description=description.strip() if description else existing.description,
            created_at=existing.created_at,  # Keep original creation time
            updated_at=datetime.now(),  # Update the modification time
        )
        updated.validate()
        self.repository.update(updated)
        return updated
