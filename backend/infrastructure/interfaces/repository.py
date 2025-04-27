from abc import ABC, abstractmethod
from typing import Any

from pydantic import UUID4


class RepositoryInterface[ModelType](ABC):
    @abstractmethod
    async def get_item(self, item_id: int) -> ModelType | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_items(self) -> list[ModelType] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_attribute(
        self, attribute: str, value: Any
    ) -> list[ModelType] | None:
        raise NotImplementedError

    @abstractmethod
    async def add_item(self, **kwargs: int) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def delete_item(self, item: ModelType) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_item(
        self, item_id: int | str, **update_values: str | int | UUID4
    ) -> ModelType:
        raise NotImplementedError