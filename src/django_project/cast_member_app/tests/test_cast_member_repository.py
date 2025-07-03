import uuid
import pytest

from src.core.cast_member.domain.cast_member import CastMember, Type
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberModel


@pytest.mark.django_db
class TestSave:
    def test_save_cast_member_in_database(self):
        cast_member = CastMember(name="Paulo", type=Type.ACTOR)
        cast_member_repository = DjangoORMCastMemberRepository()

        cast_member_repository.save(cast_member)
        cast_member_model = CastMemberModel.objects.first()

        assert CastMemberModel.objects.count() == 1
        assert cast_member_model.id == cast_member.id
        assert cast_member_model.name == cast_member.name
        assert cast_member_model.type == cast_member.type


@pytest.mark.django_db
class TestGetById:
    def test_get_not_found_cast_member(self):
        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member_model = cast_member_repository.get_by_id(uuid.uuid4())

        assert cast_member_model is None

    def test_get_cast_member_by_id(self):
        cast_member_repository = DjangoORMCastMemberRepository()
        cast_member = CastMember(name="Paulo", type=Type.ACTOR)
        cast_member_repository.save(cast_member)

        cast_member_model = cast_member_repository.get_by_id(id=cast_member.id)

        assert cast_member_model is not None
        assert cast_member_model.id == cast_member.id
        assert cast_member_model.name == cast_member.name
        assert cast_member_model.type == cast_member.type


@pytest.mark.django_db
class TestFindAll:
    def test_empty_cast_members(self):
        cast_member_repository = DjangoORMCastMemberRepository()

        cast_members = cast_member_repository.find_all()

        assert len(cast_members) == 0
        assert cast_members == []

    def test_get_all_cast_members_from_database(self):
        cast_member_repository = DjangoORMCastMemberRepository()

        cast_member_director = CastMember(name="Paulo", type=Type.DIRECTOR)
        cast_member_repository.save(cast_member_director)

        cast_member_actor = CastMember(name="Fabrício", type=Type.ACTOR)
        cast_member_repository.save(cast_member_actor)

        cast_members = cast_member_repository.find_all()

        assert len(cast_members) == 2
        assert cast_member_director.id == cast_members[0].id
        assert cast_member_director.name == cast_members[0].name
        assert cast_member_director.type == cast_members[0].type

        assert cast_member_actor.id == cast_members[1].id
        assert cast_member_actor.name == cast_members[1].name
        assert cast_member_actor.type == cast_members[1].type
