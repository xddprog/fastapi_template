from typing import Any
from pydantic import BaseModel
from sqlalchemy.orm import MappedColumn
from backend.core.repositories.base import SqlAlchemyRepository

from backend.infrastructure.interfaces.repository import RepositoryInterface


class BaseDbModelService[RepositoryType]:
    def __init__(
        self, repository: RepositoryType
    ):
        self.repository = repository
    