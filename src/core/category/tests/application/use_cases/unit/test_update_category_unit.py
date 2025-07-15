from unittest.mock import create_autospec
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
)
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(name="Filme", description="Filmes em geral", is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        input = UpdateCategory.Input(id=category.id, name="Série")

        use_case.execute(input)

        assert category.name == "Série"
        assert category.description == "Filmes em geral"
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_description(self):
        category = Category(name="Filme", description="Filmes em geral", is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        input = UpdateCategory.Input(id=category.id, description="Séries em geral")

        use_case.execute(input)

        assert category.name == "Filme"
        assert category.description == input.description
        mock_repository.update.assert_called_once_with(category)

    def test_can_deactivate_category(self):
        category = Category(name="Filme", description="Filmes em geral", is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        input = UpdateCategory.Input(id=category.id, is_active=False)

        use_case.execute(input)

        assert category.name == "Filme"
        assert category.description == "Filmes em geral"
        assert category.is_active is False
        mock_repository.update.assert_called_once_with(category)

    def test_can_activate_category(self):
        category = Category(
            name="Filme", description="Filmes em geral", is_active=False
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        input = UpdateCategory.Input(id=category.id, is_active=True)

        use_case.execute(input)

        assert category.name == "Filme"
        assert category.description == "Filmes em geral"
        assert category.is_active is True
        mock_repository.update.assert_called_once_with(category)
