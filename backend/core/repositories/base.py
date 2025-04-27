from typing import Any
from pydantic import UUID4
from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import MappedColumn
from backend.infrastructure.interfaces.repository import RepositoryInterface


class SqlAlchemyRepository[ModelType](RepositoryInterface[ModelType]):
    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self.session = session
        self.model = model

    async def get_item(self, item_id: int) -> ModelType:
        item = await self.session.get(self.model, item_id)
        return item

    async def get_all_items(self) -> list[ModelType]:
        query = select(self.model)
        items: Result = await self.session.execute(query)
        return items.scalars().all()

    async def get_by_attribute(self, attribute: str, value: str, one: bool = False) -> list[ModelType] | None:
        query = select(self.model).where(getattr(self.model, attribute) == value)
        items: Result = await self.session.execute(query)
        return items.scalars().all() if not one else items.scalar_one_or_none()

    async def add_item(self, **kwargs: int) -> ModelType:
        item = self.model(**kwargs)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete_item(self, item: ModelType) -> None:
        await self.session.delete(item)
        await self.session.commit()

    async def update_item(self, item_id: int, **update_values) -> ModelType:
        query = (
            update(self.model)
            .where(self.model.id == item_id)
            .values(update_values)
            .returning(self.model)
        )
        item: Result = await self.session.execute(query)
        await self.session.commit()
        item = item.scalars().all()[0]
        await self.session.refresh(item)
        return item

    async def get_model(self, **kwargs: int) -> ModelType:
        return self.model(**kwargs)

    async def refresh_item(self, item: ModelType):
        return await self.session.refresh(item)
