from dataclasses import dataclass
from uuid import UUID
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class UpdateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: UpdateCategoryRequest) -> None:
        category = self.repository.get_by_id(request.id)

        if not category:
            raise CategoryNotFound

        category.update_category(
            name=request.name or category.name,
            description=request.description or category.description,
        )

        if request.is_active is True:
            category.activate()

        elif request.is_active is False:
            category.deactivate()

        self.repository.update(category)
