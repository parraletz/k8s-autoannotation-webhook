import random
from logging import getLogger

from fastapi import APIRouter, HTTPException, status

from app.api.di import Container
from app.api.schemas import ItemCreateRequest, ItemResponse, ItemUpdateRequest
from app.domain.errors import NotFoundError

logger = getLogger(__name__)


def get_router(container: Container) -> APIRouter:
    router = APIRouter(prefix="/items", tags=["items"])

    @router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
    def create_item(body: ItemCreateRequest):
        generated_id = str(random.randint(1, 100))
        try:
            item = container.add_item_service.execute(
                generated_id, body.name, body.description, body.price
            )
            logger.info("Item created: %s", item)
            return ItemResponse(
                id=str(item.id),
                name=item.name,
                description=item.description,
                price=item.price,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @router.get("", response_model=list[ItemResponse])
    def get_items():
        try:
            items = container.list_items_service.execute()
            return [
                ItemResponse(
                    id=str(item.id),
                    name=item.name,
                    description=item.description,
                    price=item.price,
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                )
                for item in items
            ]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @router.get("/{id}", response_model=ItemResponse)
    def get_item(id: int):
        try:
            item = container.get_item_service.execute(id)
            return ItemResponse(
                id=str(item.id),
                name=item.name,
                description=item.description,
                price=item.price,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
        except NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(id: int):
        try:
            container.delete_item_service.execute(id)
        except NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @router.patch("/{id}", response_model=ItemResponse)
    def update_item(id: int, body: ItemUpdateRequest):
        try:
            item = container.update_item_service.execute(
                id, body.name, body.description, body.price
            )
            return ItemResponse(
                id=str(item.id),
                name=item.name,
                description=item.description,
                price=item.price,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
        except NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return router
