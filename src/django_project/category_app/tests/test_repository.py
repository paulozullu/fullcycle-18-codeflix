import pytest
from src.core.category.domain.category import Category
from src.django_project.repository import DjangoORMCategoryRepository
from src.django_project.category_app.models import Category as CategoryModel


@pytest.mark.django_db
class TestSave:
    def test_save_category_in_database(
        self,
    ):
        category = Category(name="Filme", description="Filmes em geral", is_active=True)
        repository = DjangoORMCategoryRepository()

        repository.save(category)
        category_from_db = CategoryModel.objects.first()

        assert CategoryModel.objects.count() == 1
        assert category_from_db.name == category.name
        assert category_from_db.description == category.description
        assert category_from_db.is_active == category.is_active
