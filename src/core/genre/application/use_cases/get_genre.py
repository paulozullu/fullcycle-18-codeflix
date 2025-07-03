from dataclasses import dataclass
from uuid import UUID

from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.domain.genre_repository import GenreRepository


class GetGenre:
    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        id: UUID
        name: str
        is_active: bool
        categories: set[UUID]

    def __init__(self, repository: GenreRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        genre = self.repository.get_by_id(input.id)

        if genre is None:
            raise GenreNotFound("Genre with id = {request.id} not found")

        return self.Output(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
            categories=genre.categories
        )
