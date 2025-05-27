from unittest.mock import create_autospec
import uuid
import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    repository =  create_autospec(GenreRepository)
    repository.find_all.return_value = [romance_genre, action_genre]


@pytest.fixture
def romance_genre() -> Genre:
    return Genre(
        name="Romance",
        categories={uuid.uuid4()}
    )


@pytest.fixture
def action_genre() -> Genre:
    return Genre(
        name="Action",
        categories={uuid.uuid4()}
    )

@pytest.fixture
def mock_genre_repository_without_categories() -> GenreRepository:
    repository =  create_autospec(GenreRepository)
    repository.find_all.return_value = [
        Genre(
            name="Action",
            categories=set()
        ),
        Genre(
            name="Romance",
            categories=set()
        )
    ]
    return repository


@pytest.fixture
def mock_empty_genre_repository() -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.find_all.return_value = []
    return repository


class TestListGenre:

    def test_list_genres_with_no_categories(self, mock_empty_genre_repository):
        use_case = ListGenre(mock_empty_genre_repository)
        output = use_case.execute(ListGenre.Input())

        assert output == ListGenre.Output(data=[])