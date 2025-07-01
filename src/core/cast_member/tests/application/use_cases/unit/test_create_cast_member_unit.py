from unittest.mock import create_autospec
from uuid import UUID
import pytest

from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMember
from src.core.cast_member.domain.cast_member import Type
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@pytest.fixture
def mock_cast_member_repository() -> CastMemberRepository:
    return create_autospec(CastMemberRepository)


class TestCreateCastMember:

    def test_when_created_cast_member_is_invalid(
        self,
        mock_cast_member_repository,
    ):
        use_case = CreateCastMember(
            repository=mock_cast_member_repository,
        )
        input = CreateCastMember.Input(name="", type=Type.DIRECTOR)

        with pytest.raises(InvalidCastMember, match="name cannot be empty") as exc_info:
            use_case.execute(input)

    def test_create_cast_member(self, mock_cast_member_repository):
        use_case = CreateCastMember(repository=mock_cast_member_repository)
        input = CreateCastMember.Input(name="De Niro", type=Type.ACTOR)

        output = use_case.execute(input)

        assert isinstance(output.id, UUID)
