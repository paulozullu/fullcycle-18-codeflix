import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateAndEditCastMember:
    def test_user_can_create_and_edit_cast_member(
        self,
    ) -> None:
        """
        Test the user can create and edit a cast member.
        """
        api_client = APIClient()

        # Verify list is empty
        list_response = api_client.get("/api/cast_members/")
        assert list_response.status_code == 200
        assert list_response.data == {"data": []}

        # Create a new cast_member
        response = api_client.post(
            "/api/cast_members/",
            data={
                "name": "Paulo",
                "type": "ACTOR",
            },
            content_type="application/json",
        )
        assert response.status_code == 201

        created_cast_member_id = response.data["id"]

        # Verify the cast_member is created
        list_response = api_client.get("/api/cast_members/")
        assert list_response.data == {
            "data": [
                {
                    "id": created_cast_member_id,
                    "name": "Paulo",
                    "type": "ACTOR",
                }
            ]
        }

        # Remove the cast_member
        response = api_client.delete(
            f"/api/cast_members/{created_cast_member_id}/",
        )
        assert response.status_code == 204

        # Verify the cast_member is removed
        list_response = api_client.get("/api/cast_members/")
        assert list_response.data == {"data": []}
