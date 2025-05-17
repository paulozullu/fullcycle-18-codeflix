from abc import ABC, abstractmethod
from uuid import UUID

from src.core.genre.domain.genre import Genre


class GenreRepository(ABC):
    @abstractmethod
    def get_by_id(self, id) -> Genre | None:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[Genre]:
        raise NotImplementedError

    @abstractmethod
    def save(self, genre: Genre) -> UUID:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, genre: Genre) -> None:
        raise NotImplementedError
