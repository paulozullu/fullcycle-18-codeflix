import pytest
from src.core.category.domain.category import Category
from uuid import UUID, uuid4


class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError):
            Category()

    def test_name_has_less_than_255_characters(self):
        with pytest.raises(
            ValueError, match="name cannot be longer than 255"
        ):
            Category(name="a" * 256)

    def test_category_must_be_created_with_id_as_uuid(self):
        category = Category(name="Category")
        assert isinstance(category.id, UUID)

    def test_created_category_with_default_values(self):
        category = Category(name="Category")
        assert category.name == "Category"
        assert category.description == ""
        assert category.is_active is True

    def test_category_is_created_as_active_by_default(self):
        category = Category(name="Category")
        assert category.is_active is True

    def category_is_created_with_provided_values(self):
        cat_id = uuid4()
        category = Category(
            name="Category", id=cat_id, description="Description", is_active=False
        )
        assert category.name == "Category"
        assert category.description == "Description"
        assert category.is_active is True
        assert category.id == cat_id

    def test_str(self):
        category = Category(name="Category")
        str_category = str(category)
        assert str_category == "Category -  (True)"

    def test_repr(self):
        cat_id = uuid4()
        category = Category(name="Category", id=cat_id)
        repr_category = repr(category)
        assert repr_category == f"Category ({cat_id})", cat_id

    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")

    def test_description_have_less_than_1024_characters(self):
        with pytest.raises(ValueError, match="description cannot be longer than 1024"):
            Category(name="Movie", description="a" * 1025)

    def test_name_and_description_are_invalid(self):
        with pytest.raises(
            ValueError,
            match="name cannot be empty, description cannot be longer than 1024",
        ):
            Category(name="", description="a" * 1025)


class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name="Filme", description="Filmes em geral")

        category.update_category(name="Série", description="Séries em geral")

        assert category.name == "Série"
        assert category.description == "Séries em geral"

    def test_update_category_with_invalid_name_raises_exception(self):
        category = Category(name="Filme", description="Filmes em geral")

        with pytest.raises(
            ValueError, match="name cannot be longer than 255"
        ):
            category.update_category(name="a" * 256, description="Séries em geral")

    def test_cannot_update_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            category = Category(name="Filme", description="Filmes em geral")
            category.update_category(name="", description="Séries em geral")


class TestActivate:
    def test_activte_inactive_category(self):
        category = Category(
            name="Filme", description="Filmes em geral", is_active=False
        )

        category.activate()

        assert category.is_active is True

    def test_activate_active_category(self):
        category = Category(name="Filme", description="Filmes em geral", is_active=True)

        category.activate()

        assert category.is_active is True


class TestDeactivate:
    def test_deactivate_active_category(self):
        category = Category(name="Filme", description="Filmes em geral", is_active=True)

        category.deactivate()

        assert category.is_active is False

    def test_deactivate_inactive_category(self):
        category = Category(
            name="Filme", description="Filmes em geral", is_active=False
        )

        category.deactivate()

        assert category.is_active is False


class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(slef):
        common_id = uuid4()
        category_1 = Category(name="Filme", id=common_id)
        category_2 = Category(name="Filme", id=common_id)

        assert category_1 == category_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid4()
        category = Category(name="Filme", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert category != dummy
