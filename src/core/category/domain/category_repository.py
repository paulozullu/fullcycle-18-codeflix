from abc import ABC, abstractmethod
from uuid import UUID

from src.core.category.domain.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def get_by_id(self, id) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    def save(self, category) -> UUID:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, category) -> None:
        raise NotImplementedError
