import uuid
import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain import genre_repository
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.models import Genre as GenreModel


@pytest.mark.django_db
class TestSave:
    def test_save_genre_without_categories_in_database(self):
        genre = Genre(name="Action")
        genre_repository = DjangoORMGenreRepository()

        genre_repository.save(genre)
        genre_model = GenreModel.objects.first()

        assert GenreModel.objects.count() == 1
        assert genre_model.id == genre.id
        assert genre_model.name == genre.name
        assert genre_model.is_active

    def test_save_genre_with_categories_in_database(self):
        genre_repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        category = Category(name="Movie")
        category_repository.save(category)

        genre = Genre(name="Romance")
        genre.add_category(category.id)

        assert GenreModel.objects.count() == 0
        genre_repository.save(genre)
        assert GenreModel.objects.count() == 1

        genre_model = GenreModel.objects.get(id=genre.id)
        related_category = genre_model.categories.get()
        assert related_category.id == category.id
        assert related_category.name == category.name


@pytest.mark.django_db
class TestGetById:
    def test_get_not_found_genre(self):
        genre_repository = DjangoORMGenreRepository()
        genre_model = genre_repository.get_by_id(uuid.uuid4())

        assert genre_model is None

    def test_get_genre_by_id(self):
        genre_repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        category = Category(name="Movie")
        category_repository.save(category)

        genre = Genre(name="Romance")
        genre.add_category(category.id)
        genre_repository.save(genre)

        genre_model = genre_repository.get_by_id(id=genre.id)

        assert genre_model is not None
        assert genre_model.id == genre.id
        assert genre_model.name == genre.name
        assert genre_model.is_active
        assert genre_model.categories == genre.categories


@pytest.mark.django_db
class TestFindAll:
    def test_empty_genres(self):
        genre_repository = DjangoORMGenreRepository()

        genres = genre_repository.find_all()

        assert len(genres) == 0

    def test_get_all_genres_from_database(self):
        genre_repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        category_movie = Category(name="Movie")
        category_repository.save(category_movie)

        category_documentary = Category(name="Documentary")
        category_repository.save(category_documentary)

        genre_romance = Genre(name="Romance", is_active=False)
        genre_romance.add_category(category_movie.id)
        genre_repository.save(genre_romance)

        genre_action = Genre(name="Action")
        genre_action.add_category(category_movie.id)
        genre_action.add_category(category_documentary.id)
        genre_repository.save(genre_action)

        genres = genre_repository.find_all()

        assert len(genres) == 2
        assert genre_romance.id == genres[0].id
        assert genre_romance.name == genres[0].name
        assert genre_romance.categories == genres[0].categories
        assert genre_romance.is_active == genres[0].is_active

        assert genre_action.id == genres[1].id
        assert genre_action.name == genres[1].name
        assert genre_action.categories == genres[1].categories
        assert genre_action.is_active == genres[1].is_active

