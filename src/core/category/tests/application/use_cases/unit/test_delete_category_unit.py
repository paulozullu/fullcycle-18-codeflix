from unittest.mock import create_autospec
import uuid

import pytest

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category


class TestDeleteCategory:
    def test_delete_category(self):
        category = Category(name="Filme", description="Categoria de Filmes")

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = DeleteCategory(mock_repository)
        use_case.execute(DeleteCategoryRequest(category.id))

        mock_repository.delete.assert_called_once_with(category.id)

    def test_when_category_not_found_raise_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteCategory(mock_repository)

        with pytest.raises(CategoryNotFound):
            use_case.execute(DeleteCategoryRequest(uuid.uuid4()))

        mock_repository.delete.assert_not_called()
        assert mock_repository.delete.called is False
