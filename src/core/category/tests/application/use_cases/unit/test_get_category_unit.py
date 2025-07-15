from unittest.mock import create_autospec

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.get_category import (
    GetCategory,
)
from src.core.category.domain.category import Category


class TestGetCategory:
    def test_return_found_category(self):
        category = Category(name="Filme", description="Filmes em geral", is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = GetCategory(repository=mock_repository)
        input = GetCategory.Input(id=category.id)

        response = use_case.execute(input)

        assert response == GetCategory.Output(
            id=category.id,
            name="Filme",
            description="Filmes em geral",
            is_active=True,
        )
