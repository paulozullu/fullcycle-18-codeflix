from curses import meta
from dataclasses import dataclass
from uuid import UUID
from src.config import DEFAULT_PAGINATION_SIZE
from src.core._shared.list_use_case import ListOutputMeta, ListRequest
from src.core.cast_member.domain.cast_member import Type
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: Type


class ListCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Output:
        data: list[CastMemberOutput]
        meta: ListOutputMeta

    @dataclass
    class Input(ListRequest): ...

    def execute(self, input: Input) -> Output:
        cast_members = self.repository.find_all()

        mapped_cast_members = sorted(
            [
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type,
                )
                for cast_member in cast_members
            ],
            key=lambda cast_member: getattr(cast_member, input.order_by),
        )

        page_offset = (input.current_page - 1) * DEFAULT_PAGINATION_SIZE
        cast_members_page = mapped_cast_members[
            page_offset : page_offset + DEFAULT_PAGINATION_SIZE
        ]

        return self.Output(
            data=cast_members_page,
            meta=ListOutputMeta(
                total=len(mapped_cast_members),
                current_page=input.current_page,
                per_page=input.per_page,
            ),
        )
