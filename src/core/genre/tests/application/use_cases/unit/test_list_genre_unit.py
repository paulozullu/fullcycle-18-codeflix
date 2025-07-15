from unittest.mock import create_autospec
import uuid
import pytest

from src.core._shared.list_use_case import ListOutputMeta
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def romance_genre() -> Genre:
    return Genre(name="Romance", categories={uuid.uuid4()})


@pytest.fixture
def action_genre() -> Genre:
    return Genre(name="Action", categories={uuid.uuid4()})


@pytest.fixture
def mock_genre_repository(romance_genre, action_genre) -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.find_all.return_value = [romance_genre, action_genre]
    return repository


@pytest.fixture
def mock_genre_repository_without_categories() -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.find_all.return_value = [
        Genre(name="Romance", categories=set()),
        Genre(name="Action", categories=set()),
    ]
    return repository


@pytest.fixture
def mock_empty_genre_repository() -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.find_all.return_value = []
    return repository


class TestListGenre:

    def test_list_empty_genres(self, mock_empty_genre_repository):
        use_case = ListGenre(mock_empty_genre_repository)
        output = use_case.execute(ListGenre.Input())

        assert output == ListGenre.Output(
            data=[],
            meta=ListOutputMeta(
                total=0,
                current_page=1,
                per_page=2,
            ),
        )

    def test_list_genres_with_categories(
        self, mock_genre_repository, romance_genre, action_genre
    ):
        use_case = ListGenre(mock_genre_repository)
        input = ListGenre.Input()
        output = use_case.execute(input)

        assert len(output.data) == 2
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=action_genre.id,
                    name=action_genre.name,
                    is_active=True,
                    categories=action_genre.categories,
                ),
                GenreOutput(
                    id=romance_genre.id,
                    name=romance_genre.name,
                    is_active=True,
                    categories=romance_genre.categories,
                ),
            ],
            meta=ListOutputMeta(
                total=2,
                current_page=1,
                per_page=2,
            ),
        )

    def test_list_genres_without_categories(
        self, mock_genre_repository_without_categories
    ):
        use_case = ListGenre(mock_genre_repository_without_categories)
        input = ListGenre.Input()
        output = use_case.execute(input)

        assert len(output.data) == 2
        assert output.data[0].categories == set()
        assert output.data[0].name == "Action"
        assert output.data[1].categories == set()
        assert output.data[1].name == "Romance"
        assert output.meta == ListOutputMeta(
            total=2,
            current_page=1,
            per_page=2,
        )
