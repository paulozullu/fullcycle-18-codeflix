from unittest.mock import create_autospec

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
    ListCategoriesRequest,
    ListCategoryResponse,
    ListOutputMeta,
)
from src.core.category.domain.category import Category


class TestListCategory:
    def test_return_created_categories(self):
        category = Category(name="Filme", description="Filmes em geral", is_active=True)
        category2 = Category(
            name="Série", description="Séries em geral", is_active=True
        )
        category3 = Category(
            name="Documentário", description="Documentários em geral", is_active=True
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.find_all.return_value = [
            category,
            category2,
            category3,
        ]

        use_case = ListCategory(repository=mock_repository)
        request = ListCategoriesRequest()

        response = use_case.execute(request)
        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category3.id,
                    name=category3.name,
                    description=category3.description,
                    is_active=category3.is_active,
                ),
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                ),
            ],
            meta=ListOutputMeta(current_page=1, per_page=request.per_page, total=3),
        )
        assert len(response.data) == 2
        mock_repository.find_all.assert_called_once()

    def test_return_empty_list(self):
        mock_repository = create_autospec(CategoryRepository)
        use_case = ListCategory(repository=mock_repository)
        request = ListCategoriesRequest()

        response = use_case.execute(request)
        assert response == ListCategoryResponse(
            data=[],
            meta=ListOutputMeta(),
        )
        assert len(response.data) == 0
        mock_repository.find_all.assert_called_once()
