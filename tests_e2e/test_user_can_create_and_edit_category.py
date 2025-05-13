import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_edit_category(
        self,
    ) -> None:
        """
        Test the user can create and edit a category.
        """
        api_client = APIClient()

        # Verify list is empty
        list_response = api_client.get("/api/categories/")
        assert list_response.status_code == 200
        assert list_response.data == {"data": []}

        # Create a new category
        response = api_client.post(
            "/api/categories/",
            data={
                "name": "Movie",
                "description": "Movie description",
                "is_active": True,
            },
            content_type="application/json",
        )
        assert response.status_code == 201

        created_category_id = response.data["id"]

        # Verify the category is created
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                }
            ]
        }

        # Edit the category
        response = api_client.put(
            f"/api/categories/{created_category_id}/",
            data={
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": False,
            },
            content_type="application/json",
        )
        assert response.status_code == 204

        # Verify the category is updated
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Documentary",
                    "description": "Documentary description",
                    "is_active": False,
                }
            ]
        }
