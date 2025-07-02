from uuid import UUID
import pytest

from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMember,
)
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMember
from src.core.cast_member.domain.cast_member import Type
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class TestCreateCastMember:
    def test_create_cast_member_with_valid_data(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)
        input = CreateCastMember.Input(name="Paulo", type=Type.ACTOR)

        output = use_case.execute(input)

        assert output is not None
        assert isinstance(output, CreateCastMember.Output)
        assert isinstance(output.id, UUID)
        assert len(repository.cast_members) == 1

        saved_cast_members = repository.cast_members[0]
        assert saved_cast_members.id == output.id
        assert saved_cast_members.name == "Paulo"
        assert saved_cast_members.type == Type.ACTOR

    def test_create_cast_members_with_invalid_data(self):
        use_case = CreateCastMember(repository=InMemoryCastMemberRepository())
        input = CreateCastMember.Input(name="", type=Type.ACTOR)

        with pytest.raises(
            InvalidCastMember, match="name cannot be empty"
        ) as exec_info:
            use_case.execute(input)

        assert exec_info.type == InvalidCastMember
        assert str(exec_info.value) == "name cannot be empty"
