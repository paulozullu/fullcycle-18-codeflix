from uuid import uuid4
import uuid
from venv import create
import pytest
from rest_framework.test import APIClient
from rest_framework import status

from src.django_project.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category


@pytest.fixture
def category_movie():
    return Category(
        name="Movie",
        description="Moview description",
        is_active=True,
    )


@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary description",
        is_active=True,
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestCategoryAPI:
    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        """
        Test the list categories API endpoint.
        """
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        categories = category_repository.find_all()

        expected_data = {
            "data": [
                {
                    "id": str(categories[0].id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active,
                },
                {
                    "id": str(categories[1].id),
                    "name": category_documentary.name,
                    "description": category_documentary.description,
                    "is_active": category_documentary.is_active,
                },
            ]
        }

        url = "/api/categories/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        assert response.data == expected_data


@pytest.mark.django_db
class TestRetrieveAPI:
    def test_return_400_when_id_is_invalid(
        self,
    ) -> None:
        url = "/api/categories/invalid-uuid/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_category_when_exists(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        saved_categories = category_repository.find_all()
        documentary = next(
            cat for cat in saved_categories if cat.name == category_documentary.name
        )

        url = f"/api/categories/{documentary.id}/"
        response = APIClient().get(url)

        expected_data = {
            "data": {
                "id": str(documentary.id),
                "name": category_documentary.name,
                "description": category_documentary.description,
                "is_active": category_documentary.is_active,
            }
        }
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_return_404_when_category_does_not_exist(self) -> None:
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data is None


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payload_is_invalid_then_return_400(
        self,
    ) -> None:
        url = "/api/categories/"
        response = APIClient().post(url, data={"invalid": "data"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_payload_is_valid_then_return_201(
        self,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        url = "/api/categories/"
        payload = {
            "name": "Movie",
            "description": "Movie description",
            "is_active": True,
        }
        response = APIClient().post(url, data=payload)
        created_category_id = uuid.UUID(response.data["id"])
        category = category_repository.get_by_id(created_category_id)

        assert response.status_code == status.HTTP_201_CREATED
        assert category is not None

        assert category_repository.find_all() == [
            Category(
                id=created_category_id,
                name=payload["name"],
                description=payload["description"],
                is_active=payload["is_active"],
            )
        ]


@pytest.mark.django_db
class TestUpdateAPI:
    def test_return_400_when_payload_is_invalid(
        self,
    ) -> None:
        url = "/api/categories/invalid-uuid/"
        response = APIClient().put(
            url,
            data={"name": "", "description": "Movie description", "is_active": True},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["name"] == ["This field may not be blank."]
        assert response.data["id"] == ["Must be a valid UUID."]

    def test_update_category(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        payload = {
            "name": "Updated Movie",
            "description": "Updated description",
            "is_active": False,
        }
        response = APIClient().put(url, data=payload)

        updated_category = category_repository.get_by_id(category_movie.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert updated_category.name == payload["name"]
        assert updated_category.description == payload["description"]
        assert updated_category.is_active == payload["is_active"]

    def test_return_404_when_category_does_not_exist(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f"/api/categories/{uuid4()}/"
        payload = {
            "name": "Updated Movie",
            "description": "Updated description",
            "is_active": False,
        }
        response = APIClient().put(url, data=payload)

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestDeleteAPI:
    def test_return_400_when_id_is_invalid(
        self,
    ) -> None:
        url = "/api/categories/invalid-uuid/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_204_when_category_exists(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert category_repository.get_by_id(category_movie.id) is None
        assert category_repository.find_all() == []

    def test_return_404_when_category_does_not_exist(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f"/api/categories/{uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestPatchCategory:
    def test_patch_category(self, category_movie: Category, category_repository: DjangoORMCategoryRepository) -> None:
        """
        Test the patch category API endpoint.
        """
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        payload = {
            "name": "Updated Movie",
            "is_active": False,
        }
        response = APIClient().patch(url, data=payload)

        updated_category = category_repository.get_by_id(category_movie.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert updated_category.name == payload["name"]
        assert updated_category.description == category_movie.description
        assert updated_category.is_active == payload["is_active"]

    def test_return_404_when_category_does_not_exist(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f"/api/categories/{uuid4()}/"
        payload = {
            "name": "Updated Movie",
        }
        response = APIClient().patch(url, data=payload)

        assert response.status_code == status.HTTP_404_NOT_FOUND

