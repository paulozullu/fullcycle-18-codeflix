from http import HTTPStatus
import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from rest_framework.test import APIClient


@pytest.fixture
def category_movie(category_repository):
    category_movie = Category(name="Movie", description="Movie description")
    category_repository.save(category_movie)
    return category_movie


@pytest.fixture
def category_documentary(category_repository):
    category_documentary = Category(
        name="Documentary", description="Documentary description"
    )
    category_repository.save(category_documentary)
    return category_documentary


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    category_repository = DjangoORMCategoryRepository()
    return category_repository


@pytest.fixture
def genre_romance(category_movie, category_documentary) -> Genre:
    return Genre(
        name="Romance",
        categories={category_movie.id, category_documentary.id},
        is_active=True,
    )


@pytest.fixture
def genre_drama() -> Genre:
    return Genre(
        name="Drama",
        categories=set(),
    )


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_genres_and_categories(
        self,
        genre_repository,
        genre_romance,
        genre_drama,
        category_repository,
        category_documentary,
        category_movie,
    ):
        genre_repository.save(genre_romance)
        genre_repository.save(genre_drama)
        url = "/api/genres/"
        response = APIClient().get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.data["data"]

        assert response.data["data"][0]["id"] == str(genre_romance.id)
        assert response.data["data"][0]["name"] == genre_romance.name
        assert response.data["data"][0]["is_active"] == genre_romance.is_active

        assert response.data["data"][0]["categories"]
        assert str(category_documentary.id) in response.data["data"][0]["categories"]
        assert str(category_movie.id) in response.data["data"][0]["categories"]
        assert response.data["data"][1]["id"] == str(genre_drama.id)
        assert response.data["data"][1]["name"] == genre_drama.name
        assert response.data["data"][1]["is_active"] == genre_drama.is_active
        assert response.data["data"][1]["categories"] == []

        assert response.status_code == HTTPStatus.OK
