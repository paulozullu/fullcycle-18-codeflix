from uuid import UUID
import uuid
import pytest
from src.core.category.application.use_cases.exceptions import (
    CategoryNotFound,
    InvalidCategoryData,
)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.exceptions import RelatedCategoriesNotFound
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.domain import genre_repository
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def category_repository(
    movie_category: Category, documentary_category: Category
) -> CategoryRepository:
    return InMemoryCategoryRepository(categories=[movie_category, documentary_category])


class TestCreateGenre:
    def test_create_category_with_associated_categories(
        self,
        movie_category: Category,
        documentary_category: Category,
        category_repository: CategoryRepository,
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        input = CreateGenre.Input(
            name="Action", categories={movie_category.id, documentary_category.id}
        )

        output = use_case.execute(input)
        saved_genre = genre_repository.get_by_id(output.id)

        assert isinstance(output.id, uuid.UUID)
        assert saved_genre.name == "Action"
        assert saved_genre.categories == {movie_category.id, documentary_category.id}
        assert saved_genre.is_active is True

    def test_raise_error_when_category_does_not_exist(self):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository()
        use_case = CreateGenre(
            repository=genre_repository, category_repository=category_repository
        )
        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            input = CreateGenre.Input(name="Action", categories={uuid.uuid4()})
            use_case.execute(input)

    def test_create_genre_without_categories(self):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository()
        use_case = CreateGenre(genre_repository, category_repository)
        input = CreateGenre.Input(name="Action")
        output = use_case.execute(input)
        saved_genre = genre_repository.get_by_id(output.id)

        assert isinstance(output.id, uuid.UUID)
        assert input.name == "Action"
