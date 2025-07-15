from encodings.punycode import T
from unicodedata import category
from unittest import mock
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
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestListCategory:
    def test_return_created_categories(self):
        category = Category(name="Filme", description="Filmes em geral", is_active=True)
        category2 = Category(
            name="Série", description="Séries em geral", is_active=True
        )
        category3 = Category(
            name="Documentário", description="Documentários em geral", is_active=True
        )
        repository = InMemoryCategoryRepository()
        repository.save(category)
        repository.save(category2)
        repository.save(category3)
        use_case = ListCategory(repository=repository)
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
            meta=ListOutputMeta(per_page=request.per_page, current_page=1, total=3),
        )
        assert len(response.data) == 2

    def test_return_empty_list(self):
        repository = InMemoryCategoryRepository(categories=[])
        use_case = ListCategory(repository=repository)
        request = ListCategoriesRequest()

        response = use_case.execute(request)
        assert response == ListCategoryResponse(
            data=[], meta=ListOutputMeta(current_page=1, per_page=request.per_page, total=0)
        )
        assert len(response.data) == 0
