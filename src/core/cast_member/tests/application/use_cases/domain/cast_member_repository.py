from abc import ABC, abstractmethod
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember


class CastMemberRepository(ABC):
    @abstractmethod
    def get_by_id(self, id) -> CastMember | None:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[CastMember]:
        raise NotImplementedError

    @abstractmethod
    def save(self, cast_member: CastMember) -> UUID:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, cast_member: CastMember) -> None:
        raise NotImplementedError
