import uuid
import pytest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import (
    GetCategory,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestGetCategory:
    def test_get_category_by_id(self):
        category_filme = Category(
            name="Filme", description="Filmes em geral", is_active=True
        )
        category_serie = Category(
            name="Série", description="Séries em geral", is_active=True
        )
        repository = InMemoryCategoryRepository([category_filme, category_serie])
        use_case = GetCategory(repository=repository)
        input = GetCategory.Input(id=category_filme.id)
        response = use_case.execute(input)

        assert response == GetCategory.Output(
            id=category_filme.id,
            name="Filme",
            description="Filmes em geral",
            is_active=True,
        )

    def test_when_category_does_not_exist_then_raise_exception(self):
        category_filme = Category(
            name="Filme", description="Filmes em geral", is_active=True
        )

        category_serie = Category(
            name="Série", description="Séries em geral", is_active=True
        )
        repository = InMemoryCategoryRepository([category_filme, category_serie])

        not_found_id = uuid.uuid4()
        input = GetCategory.Input(id=not_found_id)

        use_case = GetCategory(repository=repository)

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(input)
