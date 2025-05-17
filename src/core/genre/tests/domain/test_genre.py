import pytest
from uuid import UUID, uuid4

from src.core.genre.domain.genre import Genre


class TestGenre:
    def test_name_is_required(self):
        with pytest.raises(TypeError):
            Genre()

    def test_name_has_less_than_255_characters(self):
        with pytest.raises(
            ValueError, match="name should not be longer than 255 characters"
        ):
            Genre(name="a" * 256)

    def test_cannot_create_genre_with_empty_name(self):
        with pytest.raises(ValueError, match="name should not be empty"):
            Genre(name="")

    def test_created_genre_with_default_values(self):
        genre = Genre(name="Romance")
        assert genre.name == "Romance"
        assert genre.is_active is True
        assert isinstance(genre.id, UUID)
        assert genre.categories == set()

    def test_category_is_created_with_provided_values(self):
        genre_id = uuid4()
        categories = {uuid4(), uuid4()}
        genre = Genre(
            name="Romance", id=genre_id, is_active=False, categories=categories
        )
        assert genre.name == "Romance"
        assert genre.is_active is False
        assert genre.id == genre_id
        assert genre.categories == categories

    def test_genre_must_be_created_with_id_as_uuid(self):
        genre = Genre(name="Romance")
        assert isinstance(genre.id, UUID)

    def test_genre_is_created_as_active_by_default(self):
        genre = Genre(name="Romance")
        assert genre.is_active is True

    def test_str(self):
        genre = Genre(name="Romance")
        str_genre = str(genre)
        assert str_genre == "Romance - (True)"

    def test_repr(self):
        cat_id = uuid4()
        category = Genre(name="Romance", id=cat_id)
        repr_category = repr(category)
        assert repr_category == f"<Genre Romance ({cat_id})>", cat_id


class TestActivate:
    def test_activate_inactive_genre(self):
        genre = Genre(name="Romance", is_active=False)
        genre.activate()

        assert genre.is_active is True

    def test_activate_active_genre(self):
        genre = Genre(name="Romance", is_active=True)
        genre.activate()

        assert genre.is_active is True


class TestDeactivate:
    def test_deactivate_active_genre(self):
        genre = Genre(name="Romance", is_active=True)
        genre.deactivate()

        assert genre.is_active is False

    def test_deactivate_inactive_genre(self):
        genre = Genre(name="Romance", is_active=False)
        genre.deactivate()

        assert genre.is_active is False


class TestEquality:
    def test_when_genres_have_same_id_they_are_equal(self):
        common_id = uuid4()
        genre_1 = Genre(name="Romance", id=common_id)
        genre_2 = Genre(name="Romance", id=common_id)

        assert genre_1 == genre_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid4()
        genre = Genre(name="Romance", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert genre != dummy


class TestChangeName:
    def test_change_name(self):
        genre = Genre(name="Romance")
        genre.change_name("Action")

        assert genre.name == "Action"

    def test_change_name_to_empty_string(self):
        genre = Genre(name="Romance")
        with pytest.raises(ValueError, match="name should not be empty"):
            genre.change_name("")


class TestAddCategory:
    def test_add_category(self):
        genre = Genre(name="Romance")
        category_id = uuid4()

        assert category_id not in genre.categories

        genre.add_category(category_id)

        assert category_id in genre.categories

    def test_add_category_already_exists(self):
        genre = Genre(name="Romance")
        category_id = uuid4()
        genre.add_category(category_id)
        genre.add_category(category_id)

        assert len(genre.categories) == 1

class TestRemoveCategory:
    def test_remove_category(self):
        category_id = uuid4()
        genre = Genre(name="Romance", categories={category_id})

        genre.remove_category(category_id)

        assert category_id not in genre.categories

    def test_remove_category_not_exists(self):
        genre = Genre(name="Romance")
        category_id = uuid4()

        with pytest.raises(KeyError):
            genre.remove_category(category_id)
