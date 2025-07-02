from src.core.cast_member.application.use_cases.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, Type
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class TestListCastMember:
    def test_list_cast_member_with_associated_categories(self):
        cast_member_repository = InMemoryCastMemberRepository()
        cast_member = cast_member = CastMember(name="Paulo", type=Type.DIRECTOR)
        cast_member_repository.save(cast_member)
        use_case = ListCastMember(repository=cast_member_repository)

        output = use_case.execute()

        assert len(output.data) == 1
        assert output == ListCastMember.Output(
            data=[
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                )
            ]
        )

    def test_list_cast_member_when_do_not_exist_genre(self):
        cast_member_repository = InMemoryCastMemberRepository()
        use_case = ListCastMember(cast_member_repository)
        output = use_case.execute()

        assert len(output.data) == 0
        assert output == ListCastMember.Output(data=[])
