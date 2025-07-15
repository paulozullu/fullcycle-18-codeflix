from uuid import uuid4

import pytest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestUpdateCategory:
    def test_update_category_name_and_description(self):
        repository = InMemoryCategoryRepository()
        category = Category(name="Filme", description="Filmes em geral", is_active=True)
        repository.save(category)

        use_case = UpdateCategory(repository=repository)

        input = UpdateCategory.Input(
            id=category.id, name="Série", description="Séries em geral"
        )
        use_case.execute(input)

        updated_category = repository.get_by_id(category.id)

        assert updated_category.name == "Série"
        assert updated_category.description == "Séries em geral"

    def test_activate_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(
            name="Filme", description="Filmes em geral", is_active=False
        )
        repository.save(category)
        use_case = UpdateCategory(repository=repository)
        input = UpdateCategory.Input(id=category.id, is_active=True)

        use_case.execute(input)
        updated_category = repository.get_by_id(category.id)

        assert updated_category.is_active is True

    def test_deactivate_category(self):
        category = Category(name="Filme", description="Filmes em Geral", is_active=True)
        repository = InMemoryCategoryRepository()
        repository.save(category)
        input = UpdateCategory.Input(id=category.id, is_active=False)
        use_case = UpdateCategory(repository)

        use_case.execute(input)
        updated_category = repository.get_by_id(category.id)

        assert updated_category.is_active == False

    def test_update_not_found_category(self):
        category = Category(name="Filme", description="Filmes em geral")
        repository = InMemoryCategoryRepository()
        repository.save(category)
        id = uuid4()
        input = UpdateCategory.Input(id=id, name="Teste")
        use_case = UpdateCategory(repository)

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(input)

        assert exc.type == CategoryNotFound
