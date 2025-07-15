from http import HTTPStatus
import uuid
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
        category_documentary,
        category_movie,
    ):
        genre_repository.save(genre_romance)
        genre_repository.save(genre_drama)
        url = "/api/genres/"
        response = APIClient().get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.data["data"]

        assert response.data["data"][1]["id"] == str(genre_romance.id)
        assert response.data["data"][1]["name"] == genre_romance.name
        assert response.data["data"][1]["is_active"] == genre_romance.is_active
        assert response.data["data"][1]["categories"]
        assert str(category_documentary.id) in response.data["data"][1]["categories"]
        assert str(category_movie.id) in response.data["data"][1]["categories"]

        assert response.data["data"][0]["id"] == str(genre_drama.id)
        assert response.data["data"][0]["name"] == genre_drama.name
        assert response.data["data"][0]["is_active"] == genre_drama.is_active
        assert response.data["data"][0]["categories"] == []

        assert response.data["meta"]
        assert response.data["meta"]["total"] == 2
        assert response.data["meta"]["current_page"] == 1
        assert response.data["meta"]["per_page"] == 2


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_genre_with_categories(
        self,
        genre_repository: DjangoORMGenreRepository,
        category_movie,
        category_documentary,
    ):
        url = "/api/genres/"
        data = {
            "name": "Action",
            "categories": [str(category_movie.id), str(category_documentary.id)],
            "is_active": True,
        }
        response = APIClient().post(url, data, format="json")
        saved_genre = genre_repository.get_by_id(response.data["id"])

        assert response.status_code == HTTPStatus.CREATED
        assert response.data["id"]
        assert saved_genre.name == data["name"]
        assert saved_genre.is_active == data["is_active"]
        assert set(saved_genre.categories) == {
            category_movie.id,
            category_documentary.id,
        }


@pytest.mark.django_db
class TestDeleteAPI:
    def test_delete_genre(
        self,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ):
        genre_repository.save(genre_romance)
        url = f"/api/genres/{genre_romance.id}/"
        response = APIClient().delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert not genre_repository.get_by_id(genre_romance.id)

    def test_delete_non_existent_genre(self):
        genre_id = uuid.uuid4()
        url = f"/api/genres/{genre_id}/"
        response = APIClient().delete(url)

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_genre_with_invalid_id(self):
        url = "/api/genres/invalid-id/"
        response = APIClient().delete(url)

        assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_genre(
        self,
        genre_drama,
        genre_repository: DjangoORMGenreRepository,
    ):
        genre_repository.save(genre_drama)
        data = {
            "name": "Drama 2025",
            "categories": genre_drama.categories,
            "is_active": True,
        }

        url = f"/api/genres/{genre_drama.id}/"
        response = APIClient().put(url, data, format="json")

        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_when_request_data_is_invalid_then_return_400(
        self,
        genre_drama: Genre,
        genre_repository: DjangoORMGenreRepository,
    ):
        genre_repository.save(genre_drama)
        data = {
            "name": [],
            "categories": genre_drama.categories,
            "is_active": "ss",
        }
        url = f"/api/genres/{genre_drama.id}/"
        response = APIClient().put(url, data, format="json")

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        genre_drama: Genre,
        genre_repository: DjangoORMGenreRepository,
    ):
        genre_repository.save(genre_drama)
        data = {
            "name": genre_drama.name,
            "categories": {uuid.uuid4()},
            "is_active": genre_drama.is_active,
        }
        url = f"/api/genres/{genre_drama.id}/"
        response = APIClient().put(url, data, format="json")

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_when_genre_does_not_exist_then_return_404(
        self, category_documentary, category_movie
    ):
        genre_id = uuid.uuid4()

        data = {
            "name": "Drama 2025",
            "categories": {category_documentary.id, category_movie.id},
            "is_active": False,
        }
        url = f"/api/genres/{genre_id}/"

        response = APIClient().put(url, data, format="json")

        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
class TestRetrieveAPI:
    def test_retrieve_genre_and_categories(
        self,
        genre_repository,
        genre_romance,
        genre_drama,
        category_repository,
        category_documentary,
        category_movie,
    ):
        romance = genre_repository.save(genre_romance)
        genre_repository.save(genre_drama)
        url = f"/api/genres/{romance.id}/"
        response = APIClient().get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.data

        assert response.data["id"] == romance.id
        assert response.data["name"] == romance.name
        assert response.data["is_active"] == romance.is_active

        assert response.data["categories"]
        assert category_documentary.id in response.data["categories"]
