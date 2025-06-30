from uuid import UUID, uuid4
import pytest

from src.core.cast_member.domain import cast_member
from src.core.cast_member.domain.cast_member import CastMember, Type


class TestCastMember:

    def test_name_is_required(self):
        with pytest.raises(TypeError):
            CastMember(type=Type.ACTOR)

        with pytest.raises(ValueError, match="name cannot be empty"):
            CastMember(name="", type=Type.ACTOR)

    def test_name_length_not_bigger_then_255(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            CastMember(name="a" * 256, type=Type.DIRECTOR)

    def test_type_is_required(self):
        with pytest.raises(TypeError):
            CastMember(name="Robert De Niro")

    def test_type_is_valid(self):
        with pytest.raises(ValueError, match="invalid type"):
            CastMember(name="Robert De Niro", type="Producer")

    def test_cast_member_must_be_created_with_id_as_uuid(self):
        cast_member = CastMember(name="Halle Berry", type=Type.ACTOR)
        assert isinstance(cast_member.id, UUID)

    def test_created_cast_member_with_provided_values(self):
        cast_member = CastMember(name="Spike Lee", type=Type.DIRECTOR)
        assert cast_member.name == "Spike Lee"
        assert cast_member.type == Type.DIRECTOR

    def test_str(self):
        cast_member = CastMember(name="Robert De Niro", type=Type.ACTOR)
        str_cast_member = str(cast_member)
        assert str_cast_member == f"Robert De Niro - {Type.ACTOR}"

    def test_repr(self):
        cast_member = CastMember(name="Alinne Moraes", type=Type.ACTOR)
        repr_cast_member = repr(cast_member)
        assert (
            repr_cast_member == f"<Cast Member {cast_member.name} ({cast_member.type})>"
        )


class TestUpdateCastMember:
    def test_update_cast_member(self):
        cast_member = CastMember(name="Xuxa", type=Type.ACTOR)

        cast_member.update_cast_member(name="Selton Mello", type=Type.DIRECTOR)

        assert cast_member.name == "Selton Mello"
        assert cast_member.type == Type.DIRECTOR

    def test_update_cast_member_with_invalid_name_raises_exception(self):
        cast_member = CastMember(name="Xuxa", type=Type.ACTOR)

        with pytest.raises(
            ValueError, match="name cannot be longer than 255"
        ):
            cast_member.update_cast_member(name="a" * 256, type=Type.ACTOR)

    def test_cannot_update_cast_member_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            cast_member = CastMember(name="Xuxa", type=Type.ACTOR)
            cast_member.update_cast_member(name="", type=Type.ACTOR)


class TestEquality:
    def test_when_cast_members_have_same_id_they_are_equal(slef):
        common_id = uuid4()
        cast_member_1 = CastMember(
            name="Selton Mello", type=Type.DIRECTOR, id=common_id
        )
        cast_member_2 = CastMember(
            name="Selton Mello", type=Type.DIRECTOR, id=common_id
        )

        assert cast_member_1 == cast_member_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid4()
        cast_member = CastMember(name="Selton Mello", type=Type.DIRECTOR, id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert cast_member != dummy
