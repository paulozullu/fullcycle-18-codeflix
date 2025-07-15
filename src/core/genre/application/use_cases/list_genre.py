from dataclasses import dataclass
from uuid import UUID
from src.config import DEFAULT_PAGINATION_SIZE
from src.core._shared.list_use_case import ListOutputMeta, ListRequest, ListResponse
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.category_app import repository


@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]


class ListGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    @dataclass
    class Input(ListRequest): ...

    @dataclass
    class Output(ListResponse):
        data: list[GenreOutput]

    def execute(self, input: Input) -> Output:
        genres = self.repository.find_all()

        mapped_genres = sorted(
            [
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=genre.categories,
                )
                for genre in genres
            ],
            key=lambda genre: getattr(genre, input.order_by),
        )

        page_offset = (input.current_page - 1) * DEFAULT_PAGINATION_SIZE
        genres_page = mapped_genres[page_offset : page_offset + DEFAULT_PAGINATION_SIZE]

        return self.Output(
            data=genres_page,
            meta=ListOutputMeta(
                total=len(mapped_genres),
                current_page=input.current_page,
                per_page=input.per_page,
            ),
        )
