from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.core.cast_member.domain.cast_member import Type
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class UpdateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID
        name: str
        type: Type

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        cast_member = self.repository.get_by_id(id=input.id)
        if not cast_member:
            raise CastMemberNotFound(f"Cast member with {input.id} not found.")

        try:
            cast_member.update_cast_member(name=input.name, type=input.type)
        except ValueError as error:
            raise InvalidCastMember(error)

        self.repository.update(cast_member)

        return self.Output(id=cast_member.id)
