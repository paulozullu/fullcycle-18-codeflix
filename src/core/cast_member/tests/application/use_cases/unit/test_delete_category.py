from unittest.mock import create_autospec
import uuid

import pytest

from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMember,
)
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMember, Type
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestDeleteCastMember:
    def test_delete_cast_member(self):
        cast_member = CastMember(name="Paulo", type=Type.DIRECTOR)

        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = cast_member

        use_case = DeleteCastMember(mock_repository)
        use_case.execute(DeleteCastMember.Input(cast_member.id))

        mock_repository.delete.assert_called_once_with(cast_member.id)

    def test_when_cast_member__not_found_raise_exception(self):
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteCastMember(mock_repository)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(DeleteCastMember.Input(uuid.uuid4()))

        mock_repository.delete.assert_not_called()
        assert mock_repository.delete.called is False
