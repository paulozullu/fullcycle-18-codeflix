from uuid import uuid4

import pytest

from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMember,
)
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMember, Type
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


@pytest.fixture
def cast_member_repository():
    return InMemoryCastMemberRepository()


class TestDeleteCastMember:
    def test_delete_cast_member(self, cast_member_repository):
        cast_member = CastMember(name="Paulo", type=Type.DIRECTOR)
        cast_member_repository.save(cast_member)
        use_case = DeleteCastMember(repository=cast_member_repository)
        input = DeleteCastMember.Input(
            id=cast_member.id,
        )

        assert cast_member_repository.get_by_id(cast_member.id) is not None

        use_case.execute(input)

        assert cast_member_repository.find_all() == []

    def test_raise_not_found_when_delete_inexistent_cast_member(
        self, cast_member_repository
    ):
        use_case = DeleteCastMember(repository=cast_member_repository)
        input = DeleteCastMember.Input(
            id=uuid4(),
        )

        with pytest.raises(CastMemberNotFound):
            use_case.execute(input)
