from typing import Optional

from src.core.cast_member.domain.cast_member import CastMember, Type
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberModel


class DjangoORMCastMemberRepository(CastMemberRepository):
    def __init__(self, model: CastMemberModel = CastMemberModel):
        self.model = model

    def save(self, cast_member: CastMember):
        cast_member_model = CastMemberModelMapper.to_model(cast_member)
        cast_member_model.save()

    def get_by_id(self, id: str) -> Optional[CastMember]:
        try:
            cast_member_model = self.model.objects.get(id=id)
            return CastMemberModelMapper.to_entity(cast_member_model)
        except self.model.DoesNotExist:
            return None

    def delete(self, id: str):
        self.model.objects.filter(id=id).delete()

    def find_all(self) -> list[CastMember]:
        return [
            CastMemberModelMapper.to_entity(cast_member_model)
            for cast_member_model in self.model.objects.all()
        ]

    def update(self, cast_member: CastMember):
        try:
            self.model.objects.get(id=cast_member.id)
        except self.model.DoesNotExist:
            return None

        self.model.objects.filter(id=cast_member.id).update(
            name=cast_member.name,
            type=cast_member.type,
        )


class CastMemberModelMapper:
    @staticmethod
    def to_model(cast_member: CastMember) -> CastMemberModel:
        return CastMemberModel(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )

    @staticmethod
    def to_entity(cast_member_model: CastMemberModel) -> CastMember:
        return CastMember(
            id=cast_member_model.id,
            name=cast_member_model.name,
            type=Type(cast_member_model.type),
        )
