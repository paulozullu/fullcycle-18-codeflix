from uuid import UUID
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from django_project.category_app.models import Category as CategoryModel


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, model: CategoryModel = CategoryModel):
        self.model = model

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category = self.model.objects.get(id=id)
            return Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
        except self.model.DoesNotExist:
            return None

    def find_all(self) -> list[Category]:
        categories = self.model.objects.all()
        return [
            Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
            for category in categories
        ]

    def save(self, category: Category) -> Category:
        category_model = self.model.objects.create(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

        category.id = category_model.id
        return category

    def delete(self, id: UUID) -> None:
        self.model.objects.filter(id=id).delete()

    def update(self, category: Category) -> None:
        self.model.objects.filter(id=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
