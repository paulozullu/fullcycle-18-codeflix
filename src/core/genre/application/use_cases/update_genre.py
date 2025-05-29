from dataclasses import dataclass, field
from operator import is_
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class UpdateGenre:
    def __init__(
        self, repository: GenreRepository, category_repository: CategoryRepository
    ):
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        id: UUID
        name: str
        category_ids: set[UUID] = field(default_factory=set)
        is_active: bool = True

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        genre = self.repository.get_by_id(id=input.id)
        if not genre:
            raise GenreNotFound(f"Genre with {input.id} not found.")

        category_ids = {category.id for category in self.category_repository.find_all()}
        if not input.category_ids.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories {input.category_ids - category_ids} not found"
            )
        
        try:
            genre.change_name(name=input.name)
        except ValueError as error:
            raise InvalidGenre(error)

        if input.is_active:
            genre.activate()
        else:
            genre.deactivate()

        category_ids = {category.id for category in self.category_repository.find_all()}
        if not input.category_ids.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories {input.category_ids - category_ids} not found"
            )

        for category_id in set(genre.categories):
            if not category_id in input.category_ids:
                genre.remove_category(category_id)

        for category_id in set(input.category_ids):
            if not category_id in genre.categories:
                genre.add_category(category_id)

        self.repository.update(genre)

        return self.Output(id=genre.id)
