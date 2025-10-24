from dataclasses import dataclass
from functools import lru_cache

from fastapi import Depends

from app.domain.interfaces import ItemRepository
from app.handlers.item import AddItem, DeleteItem, GetItem, ListItems, UpdateItem
from app.infra.memory_repo import InMemoryRepository


@dataclass
class Container:
    repository: InMemoryRepository
    add_item_service: AddItem
    list_items_service: ListItems
    get_item_service: GetItem
    delete_item_service: DeleteItem
    update_item_service: UpdateItem


@lru_cache
def _singleton():
    repository = InMemoryRepository()
    return Container(
        repository=repository,
        add_item_service=AddItem(repository),
        list_items_service=ListItems(repository),
        get_item_service=GetItem(repository),
        delete_item_service=DeleteItem(repository),
        update_item_service=UpdateItem(repository),
    )


def build_container(reset: bool = False) -> Container:
    if reset:
        repository = InMemoryRepository()
        return Container(
            repository=repository,
            add_item_service=AddItem(repository),
            list_items_service=ListItems(repository),
            get_item_service=GetItem(repository),
            delete_item_service=DeleteItem(repository),
            update_item_service=UpdateItem(repository),
        )
    return _singleton()


def get_repository() -> ItemRepository:
    return InMemoryRepository()


def get_add_item_service(
    repo: InMemoryRepository = Depends(build_container),
) -> AddItem:
    return AddItem(repo)


def get_list_items_service(
    repo: InMemoryRepository = Depends(get_repository),
) -> ListItems:
    return ListItems(repo)


def get_get_item_service(
    repo: InMemoryRepository = Depends(get_repository),
) -> GetItem:
    return GetItem(repo)


def get_delete_item_service(
    repo: InMemoryRepository = Depends(get_repository),
) -> DeleteItem:
    return DeleteItem(repo)
