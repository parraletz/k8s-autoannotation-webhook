import pytest

from app.api.di import build_container
from app.domain.errors import NotFoundError
from app.handlers.item import AddItem, DeleteItem, GetItem, ListItems, UpdateItem


def test_happy_path():
    container = build_container(reset=True)
    add, list_items, get, delete, update = (
        AddItem(container.repository),
        ListItems(container.repository),
        GetItem(container.repository),
        DeleteItem(container.repository),
        UpdateItem(container.repository),
    )

    # Create an item
    item = add.execute("1", "pencil", "Pencil with eraser", 1.99)
    assert item.name == "pencil"
    assert item.description == "Pencil with eraser"
    assert item.price == 1.99

    # List items
    items = [i.name for i in list_items.execute()]
    assert items == ["pencil"]

    # Get item
    item = get.execute(item.id)
    assert item.name == "pencil"
    assert item.description == "Pencil with eraser"
    assert item.price == 1.99

    # Update item (passing only price)
    item = update.execute(item.id, price=2.99)
    assert item.name == "pencil"
    assert item.description == "Pencil with eraser"
    assert item.price == 2.99

    # Delete item
    delete.execute(item.id)
    with pytest.raises(NotFoundError):
        get.execute(item.id)
