from unittest.mock import create_autospec
import uuid
import pytest

from src.core.cast_member.application.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, Type
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@pytest.fixture
def mock_cast_member_repository(
    director_cast_member, actor_cast_member
) -> CastMemberRepository:
    repository = create_autospec(CastMemberRepository)
    repository.find_all.return_value = [director_cast_member, actor_cast_member]
    return repository


@pytest.fixture
def director_cast_member() -> CastMember:
    return CastMember(name="Spike Lee", type=Type.DIRECTOR)


@pytest.fixture
def actor_cast_member() -> CastMember:
    return CastMember(name="Camila Pitanga", type=Type.ACTOR)


@pytest.fixture
def mock_empty_cast_member_repository() -> CastMemberRepository:
    repository = create_autospec(CastMemberRepository)
    repository.find_all.return_value = []
    return repository


class TestListCastMember:

    def test_list_cast_members(
        self, mock_cast_member_repository, actor_cast_member, director_cast_member
    ):
        use_case = ListCastMember(repository=mock_cast_member_repository)
        output = use_case.execute()

        assert len(output.data) == 2
        assert output == ListCastMember.Output(
            data=[
                CastMemberOutput(
                    id=director_cast_member.id,
                    name=director_cast_member.name,
                    type=director_cast_member.type,
                ),
                CastMemberOutput(
                    id=actor_cast_member.id,
                    name=actor_cast_member.name,
                    type=actor_cast_member.type,
                ),
            ]
        )

    def test_list_with_empty_repository(self, mock_empty_cast_member_repository):
        use_case = ListCastMember(mock_empty_cast_member_repository)
        output = use_case.execute()

        assert output == ListCastMember.Output(data=[])
