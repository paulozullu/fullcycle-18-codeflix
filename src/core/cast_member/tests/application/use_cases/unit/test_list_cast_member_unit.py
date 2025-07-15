from unittest.mock import create_autospec
import pytest

from src.core._shared.list_use_case import ListOutputMeta
from src.core.cast_member.application.use_cases.list_cast_member import (
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
        input = ListCastMember.Input()
        output = use_case.execute(input)

        assert len(output.data) == 2
        assert output == ListCastMember.Output(
            data=[
                CastMemberOutput(
                    id=actor_cast_member.id,
                    name=actor_cast_member.name,
                    type=actor_cast_member.type,
                ),
                CastMemberOutput(
                    id=director_cast_member.id,
                    name=director_cast_member.name,
                    type=director_cast_member.type,
                ),
            ],
            meta=ListOutputMeta(
                total=2,
                current_page=1,
                per_page=2,
            ),
        )

    def test_list_with_empty_repository(self, mock_empty_cast_member_repository):
        use_case = ListCastMember(mock_empty_cast_member_repository)
        input = ListCastMember.Input()
        output = use_case.execute(input)

        assert output == ListCastMember.Output(data=[], meta=ListOutputMeta(
            total=0,
            current_page=1,
            per_page=2,
        ))
