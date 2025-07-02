from uuid import uuid4

import pytest

from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, Type
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


@pytest.fixture
def cast_member_repository():
    return InMemoryCastMemberRepository()


class TestUpdateCastMember:
    def test_update_cast_member(self, cast_member_repository):
        cast_member = CastMember(name="Paulo", type=Type.DIRECTOR)
        cast_member_repository.save(cast_member)
        use_case = UpdateCastMember(repository=cast_member_repository)
        input = UpdateCastMember.Input(
            id=cast_member.id,
            name="Fabrício",
            type=Type.ACTOR,
        )

        use_case.execute(input)
        updated_genre = cast_member_repository.get_by_id(cast_member.id)

        assert updated_genre.name == "Fabrício"
        assert updated_genre.type == Type.ACTOR

    def test_raise_not_found_when_update_inexistent_cast_member(
        self, cast_member_repository
    ):
        use_case = UpdateCastMember(repository=cast_member_repository)
        input = UpdateCastMember.Input(
            id=uuid4(),
            name="Fabrício",
            type=Type.ACTOR,
        )

        with pytest.raises(CastMemberNotFound):
            use_case.execute(input)
