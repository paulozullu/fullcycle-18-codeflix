from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    InvalidCategoryData,
)


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        input = CreateCategory.Input(
            name="Filme", description="Filmes em geral", is_active=True
        )

        response = use_case.execute(input)

        assert response.id is not None
        assert isinstance(response, CreateCategory.Output)
        assert isinstance(response.id, UUID)
        assert mock_repository.save.called

    def test_create_category_with_invalid_data(self):
        use_case = CreateCategory(repository=MagicMock(CategoryRepository))
        with pytest.raises(
            InvalidCategoryData, match="name cannot be empty"
        ) as exec_info:
            use_case.execute(CreateCategory.Input(name=""))

        assert exec_info.type == InvalidCategoryData
        assert str(exec_info.value) == "name cannot be empty"
