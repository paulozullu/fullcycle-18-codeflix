

from uuid import UUID
import pytest
from src.core.category.application.use_cases.create_category import CreateCategory
from src.core.category.application.use_cases.exceptions import InvalidCategoryData
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        input = CreateCategory.Input(
            name="Filme", description="Filmes em geral", is_active=True
        )

        response = use_case.execute(input)

        assert response is not None
        assert isinstance(response, CreateCategory.Output)
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1

        saved_category = repository.categories[0]
        assert saved_category.id == response.id
        assert saved_category.name == "Filme"
        assert saved_category.description == "Filmes em geral"
        assert saved_category.is_active

    def test_create_category_with_invalid_data(self):
        use_case = CreateCategory(repository=InMemoryCategoryRepository())
        input = CreateCategory.Input(name="")

        with pytest.raises(
            InvalidCategoryData, match="name cannot be empty"
        ) as exec_info:
            response = use_case.execute(input)

        assert exec_info.type == InvalidCategoryData
        assert str(exec_info.value) == "name cannot be empty"
