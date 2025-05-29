from unittest.mock import create_autospec
import uuid
import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class TestUpdateGenreUnit:
    @pytest.fixture
    def mock_genre_repository(self):
        return create_autospec(GenreRepository)

    @pytest.fixture
    def mock_category_repository(self):
        return create_autospec(CategoryRepository)

    def test_raise_exception_when_genre_does_not_exist(
        self, mock_genre_repository, mock_category_repository
    ):
        mock_genre_repository.get_by_id.return_value = None
        use_case = UpdateGenre(mock_genre_repository, mock_category_repository)

        with pytest.raises(GenreNotFound, match="Genre with .* not found."):
            use_case.execute(input=UpdateGenre.Input(id=uuid.uuid4(), name="Romance"))

    def test_raise_invalid_genre_exception(
        self, mock_genre_repository, mock_category_repository
    ):
        category = Category(name="Movie", description="Movie category")
        mock_category_repository.find_all.return_value = [category]
        genre = Genre(name="Romance", categories={category.id}, is_active=True)
        mock_genre_repository.get_by_id.return_value = genre
        use_case = UpdateGenre(mock_genre_repository, mock_category_repository)
        input = UpdateGenre.Input(
            id=genre.id, name="", category_ids={category.id}, is_active=genre.is_active
        )
        with pytest.raises(InvalidGenre, match="name should not be empty"):
            use_case.execute(input=input)

    def test_raise_related_categories_not_found(self, mock_genre_repository, mock_category_repository):
        category = Category(name="Movie", description="Movie category")
        new_category = Category(name="Old", description="Old movies category")
        mock_category_repository.find_all.return_value = [category]

        genre = Genre(name="Romance", categories={category.id}, is_active=True)
        mock_genre_repository.get_by_id.return_value = genre
        use_case = UpdateGenre(mock_genre_repository, mock_category_repository)
        input = UpdateGenre.Input(
            id=genre.id, name="Action", category_ids={category.id, new_category.id}, is_active=False
        )

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input=input)

    def test_should_update_genre_successfully(
            self,
            mock_genre_repository,
            mock_category_repository
    ):
        category = Category(name="Movie", description="Movie category")
        new_category = Category(name="Old", description="Old movies category")
        mock_category_repository.find_all.return_value = [category, new_category]
        genre = Genre(name="Romance", categories={category.id}, is_active=True)
        mock_genre_repository.get_by_id.return_value = genre
        use_case = UpdateGenre(mock_genre_repository, mock_category_repository)
        input = UpdateGenre.Input(
            id=genre.id, name="Action", category_ids={category.id, new_category.id}, is_active=False
        )

        use_case.execute(input=input)
        updated_genre = mock_genre_repository.get_by_id(input.id)

        assert updated_genre.id == input.id
        assert updated_genre.name == input.name
        assert updated_genre.is_active == input.is_active
        assert len(updated_genre.categories) == 2
        assert updated_genre.categories == input.category_ids
