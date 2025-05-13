from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestDeleteCategory:
    def test_delete_category(self):
        category_filme = Category(
            name="Filme", description="Filmes em geral", is_active=True
        )
        category_serie = Category(
            name="Série", description="Séries em geral", is_active=True
        )
        repository = InMemoryCategoryRepository([category_filme, category_serie])
        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(id=category_filme.id)

        assert repository.get_by_id(category_filme.id) is not None

        response = use_case.execute(request)

        assert repository.get_by_id(category_filme.id) is None

        assert response is None
