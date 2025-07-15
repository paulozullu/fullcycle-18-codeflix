from http import HTTPStatus
import uuid
import pytest

from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMember, Type
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def cast_member_actor() -> CastMember:
    return CastMember(
        name="Paulo",
        type=Type.ACTOR,
    )


@pytest.fixture
def cast_member_director() -> CastMember:
    return CastMember(
        name="Fabrício",
        type=Type.DIRECTOR,
    )


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_cast_members(
        self,
        cast_member_repository,
        cast_member_actor,
        cast_member_director,
    ):
        cast_member_repository.save(cast_member_actor)
        cast_member_repository.save(cast_member_director)
        url = "/api/cast_members/"
        response = APIClient().get(url)

        assert response.status_code == HTTPStatus.OK
        assert response.data["data"]

        assert response.data["data"][0]["id"] == str(cast_member_director.id)
        assert response.data["data"][0]["name"] == cast_member_director.name
        assert response.data["data"][0]["type"] == cast_member_director.type

        assert response.data["data"][1]["id"] == str(cast_member_actor.id)
        assert response.data["data"][1]["name"] == cast_member_actor.name
        assert response.data["data"][1]["type"] == cast_member_actor.type

        assert response.data["meta"]
        assert response.data["meta"]["total"] == 2
        assert response.data["meta"]["current_page"] == 1
        assert response.data["meta"]["per_page"] == 2


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_cast_member(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
    ):
        url = "/api/cast_members/"
        data = {"name": "Paulo", "type": Type.ACTOR}
        response = APIClient().post(url, data, format="json")
        saved_cast_member = cast_member_repository.get_by_id(response.data["id"])

        assert response.status_code == HTTPStatus.CREATED
        assert response.data["id"]
        assert data["name"] == saved_cast_member.name
        assert data["type"] == saved_cast_member.type

    def test_create_invalid_cast_member(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
    ):
        url = "/api/cast_members/"
        data = {"name": "Paulo", "type": "invalid_type"}  # Invalid type
        response = APIClient().post(url, data, format="json")

        assert "id" not in response.data
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "type" in response.data


@pytest.mark.django_db
class TestDeleteAPI:
    def test_delete_cast_member(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
        cast_member_actor: CastMember,
    ):
        cast_member_repository.save(cast_member_actor)
        url = f"/api/cast_members/{cast_member_actor.id}/"
        response = APIClient().delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert not cast_member_repository.get_by_id(cast_member_actor.id)

    def test_delete_non_existent_cast_member(self):
        cast_member_id = uuid.uuid4()
        url = f"/api/cast_members/{cast_member_id}/"
        response = APIClient().delete(url)

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_cast_member_with_invalid_id(self):
        url = "/api/cast_members/invalid-id/"
        response = APIClient().delete(url)

        assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_cast_member(
        self,
        cast_member_director,
        cast_member_repository: DjangoORMCastMemberRepository,
    ):
        cast_member_repository.save(cast_member_director)
        data = {
            "name": "Paulo",
            "type": Type.ACTOR,
        }

        url = f"/api/cast_members/{cast_member_director.id}/"
        response = APIClient().put(url, data, format="json")

        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_when_request_data_is_invalid_then_return_400(
        self,
        cast_member_director: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ):
        cast_member_repository.save(cast_member_director)
        data = {
            "name": [],
            "type": "invalid_type",
        }
        url = f"/api/cast_members/{cast_member_director.id}/"
        response = APIClient().put(url, data, format="json")

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_when_cast_member_does_not_exist_then_return_404(
        self,
    ):
        cast_member_id = uuid.uuid4()

        data = {
            "name": "Drama 2025",
            "type": Type.DIRECTOR,
        }
        url = f"/api/cast_members/{cast_member_id}/"

        response = APIClient().put(url, data, format="json")

        assert response.status_code == HTTPStatus.NOT_FOUND
