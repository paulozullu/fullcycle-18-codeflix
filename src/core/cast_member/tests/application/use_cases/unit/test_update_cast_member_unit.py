from unittest.mock import create_autospec
import uuid
import pytest

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, Type
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestUpdateCastMember:
    @pytest.fixture
    def mock_cast_member_repository(self):
        return create_autospec(CastMemberRepository)

    def test_raise_exception_when_cast_member_does_not_exist(
        self, mock_cast_member_repository
    ):
        mock_cast_member_repository.get_by_id.return_value = None
        use_case = UpdateCastMember(mock_cast_member_repository)

        with pytest.raises(CastMemberNotFound, match="Cast member with .* not found."):
            use_case.execute(
                input=UpdateCastMember.Input(
                    id=uuid.uuid4(), name="Paulo", type=Type.DIRECTOR
                )
            )

    def test_raise_invalid_cast_member_exception_with_empty_name(
        self, mock_cast_member_repository
    ):
        cast_member = CastMember(name="Paulo", type=Type.ACTOR)
        mock_cast_member_repository.get_by_id.return_value = cast_member
        use_case = UpdateCastMember(mock_cast_member_repository)
        input = UpdateCastMember.Input(id=cast_member.id, name="", type=Type.ACTOR)
        with pytest.raises(InvalidCastMember, match="name cannot be empty"):
            use_case.execute(input=input)

    def test_raise_invalid_cast_member_exception_with_invalid_name(
        self, mock_cast_member_repository
    ):
        cast_member = CastMember(name="Paulo", type=Type.ACTOR)
        mock_cast_member_repository.get_by_id.return_value = cast_member
        use_case = UpdateCastMember(mock_cast_member_repository)
        input = UpdateCastMember.Input(
            id=cast_member.id, name="a" * 256, type=Type.ACTOR
        )
        with pytest.raises(InvalidCastMember, match="name cannot be longer than 255"):
            use_case.execute(input=input)

    def test_raise_invalid_cast_member_exception_with_empty_type(
        self, mock_cast_member_repository
    ):
        cast_member = CastMember(name="Paulo", type=Type.ACTOR)
        mock_cast_member_repository.get_by_id.return_value = cast_member
        use_case = UpdateCastMember(mock_cast_member_repository)
        input = UpdateCastMember.Input(id=cast_member.id, name="Paulo", type="")
        with pytest.raises(InvalidCastMember, match="type cannot be empty"):
            use_case.execute(input=input)

    def test_raise_invalid_cast_member_exception_with_invalid_type(
        self, mock_cast_member_repository
    ):
        cast_member = CastMember(name="Paulo", type=Type.ACTOR)
        mock_cast_member_repository.get_by_id.return_value = cast_member
        use_case = UpdateCastMember(mock_cast_member_repository)
        input = UpdateCastMember.Input(id=cast_member.id, name="Paulo", type="invalido")
        with pytest.raises(InvalidCastMember, match="invalid type"):
            use_case.execute(input=input)

    def test_should_update_cast_member_successfully(self, mock_cast_member_repository):
        cast_member = CastMember(name="Paulo", type=Type.ACTOR)
        mock_cast_member_repository.get_by_id.return_value = cast_member
        use_case = UpdateCastMember(mock_cast_member_repository)
        input = UpdateCastMember.Input(
            id=cast_member.id, name="Fabrício", type=Type.DIRECTOR
        )

        use_case.execute(input=input)
        updated_cast_member = mock_cast_member_repository.get_by_id(input.id)

        assert updated_cast_member.id == input.id
        assert updated_cast_member.name == input.name
        assert updated_cast_member.type == input.type
