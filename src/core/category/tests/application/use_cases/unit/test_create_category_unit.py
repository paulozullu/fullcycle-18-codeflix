from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
    CreateCategoryResponse,
    InvalidCategoryData,
)


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(
            name="Filme", description="Filmes em geral", is_active=True
        )

        response = use_case.execute(request)

        assert response.id is not None
        assert isinstance(response, CreateCategoryResponse)
        assert isinstance(response.id, UUID)
        assert mock_repository.save.called

    def test_create_category_with_invalid_data(self):
        use_case = CreateCategory(repository=MagicMock(CategoryRepository))
        with pytest.raises(
            InvalidCategoryData, match="name should not be empty"
        ) as exec_info:
            use_case.execute(CreateCategoryRequest(name=""))

        assert exec_info.type == InvalidCategoryData
        assert str(exec_info.value) == "name should not be empty"
