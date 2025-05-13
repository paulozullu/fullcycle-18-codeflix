from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryResponse,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestSave:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(name="Filme", description="Filmes em geral")

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category


class TestGetById:
    def test_can_get_category(self):
        category = Category(name="Filme", description="Filmes em geral")
        category2 = Category(
            name="Serie", description="Series em geral", is_active=True
        )
        repository = InMemoryCategoryRepository([category, category2])
        found_category = repository.get_by_id(category.id)

        assert found_category == category


class TestDeleteById:
    def test_can_delete_category(self):
        category = Category(name="Filme", description="Filmes em geral")
        category2 = Category(
            name="Serie", description="Series em geral", is_active=True
        )

        repository = InMemoryCategoryRepository([category, category2])
        response = repository.delete(category.id)

        assert response is None