from unicodedata import category
from unittest import mock
from unittest.mock import create_autospec

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.list_categories import CategoryOutput, ListCategories, ListCategoriesRequest, ListCategoriesResponse
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestListCategories:
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
        use_case = ListCategories(repository=repository)
        request = ListCategoriesRequest()

        response = use_case.execute(request)
        
        assert response == ListCategoriesResponse(
            data=[
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                ),
                CategoryOutput(
                    id=category2.id,
                    name=category2.name,
                    description=category2.description,
                    is_active=category2.is_active,
                ),
                CategoryOutput(
                    id=category3.id,
                    name=category3.name,
                    description=category3.description,
                    is_active=category3.is_active,
                ),
            ]
        )
        assert len(response.data) == 3

    def test_return_empty_list(self):
        repository = InMemoryCategoryRepository(categories=[])
        use_case = ListCategories(repository=repository)
        request = ListCategoriesRequest()

        response = use_case.execute(request)
        assert response == ListCategoriesResponse(
            data=[]
        )
        assert len(response.data) == 0
