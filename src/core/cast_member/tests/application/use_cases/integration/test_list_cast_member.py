from src.core._shared.list_use_case import ListOutputMeta
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

        input = ListCastMember.Input()
        output = use_case.execute(input)

        assert len(output.data) == 1
        assert output == ListCastMember.Output(
            data=[
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                )
            ],
            meta=ListOutputMeta(
                total=1,
                current_page=1,
                per_page=input.per_page,
            ),
        )

    def test_list_cast_member_when_do_not_exist_genre(self):
        cast_member_repository = InMemoryCastMemberRepository()
        use_case = ListCastMember(cast_member_repository)
        input = ListCastMember.Input()
        output = use_case.execute(input)

        assert len(output.data) == 0
        assert output == ListCastMember.Output(
            data=[],
            meta=ListOutputMeta(
                total=0,
                current_page=1,
                per_page=input.per_page,
            ),
        )
