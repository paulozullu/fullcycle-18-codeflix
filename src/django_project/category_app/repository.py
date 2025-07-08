from uuid import UUID
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.django_project.category_app.models import Category as CategoryModel


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, model: CategoryModel = CategoryModel):
        self.model = model

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category_model = self.model.objects.get(id=id)
            return CategoryModelMapper.to_entity(category_model)
        except self.model.DoesNotExist:
            return None

    def find_all(self) -> list[Category]:
        category_models = self.model.objects.all()
        return [CategoryModelMapper.to_entity(category) for category in category_models]

    def save(self, category: Category) -> None:
        category_model = CategoryModelMapper.to_model(category)
        category_model.save()

    def delete(self, id: UUID) -> None:
        self.model.objects.filter(id=id).delete()

    def update(self, category: Category) -> None:
        self.model.objects.filter(id=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )


class CategoryModelMapper:
    @staticmethod
    def to_model(category: Category) -> CategoryModel:
        return CategoryModel(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

    def to_entity(category_model: CategoryModel) -> Category:
        return Category(
            id=category_model.id,
            name=category_model.name,
            description=category_model.description,
            is_active=category_model.is_active,
        )
