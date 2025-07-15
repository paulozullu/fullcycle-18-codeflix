from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound


class DeleteCategory:
    @dataclass
    class Input:
        id: UUID

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: Input) -> None:
        category = self.repository.get_by_id(request.id)

        if not category:
            raise CategoryNotFound("Category with id = {request.id} not found")

        self.repository.delete(category.id)
