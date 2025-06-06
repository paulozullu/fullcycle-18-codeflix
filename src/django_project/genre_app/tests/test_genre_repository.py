import pytest

from src.core.category.domain.category import Category
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
