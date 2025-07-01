from dataclasses import dataclass
from operator import is_
from uuid import UUID

from traitlets import Type

from src.core.cast_member.application.exceptions import InvalidCastMember
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class CreateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input:
        name: str
        type: Type

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        try:
            cast_member = CastMember(
                name=input.name, type=input.type
            )
            self.repository.save(cast_member)
        except ValueError as err:
            raise InvalidCastMember(err)

        return self.Output(id=cast_member.id)