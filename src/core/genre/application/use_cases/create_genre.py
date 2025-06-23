from dataclasses import dataclass, field
from operator import is_
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class CreateGenre:
    def __init__(self, repository: GenreRepository, category_repository: CategoryRepository):
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        name: str
        categories: set[UUID] = field(default_factory=set)
        is_active: bool = True

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        category_ids = {category.id for category in self.category_repository.find_all()}
        if not input.categories.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories {input.categories - category_ids} not found"
            )

        try:
            genre = Genre(
                name=input.name, is_active=input.is_active, categories=input.categories
            )
            self.repository.save(genre)
        except ValueError as err:
            raise InvalidGenre(err)

        return self.Output(id=genre.id)