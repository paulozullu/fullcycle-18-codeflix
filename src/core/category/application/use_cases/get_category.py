from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound


class GetCategory:

    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        id: UUID
        name: str
        description: str
        is_active: bool

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        category = self.repository.get_by_id(input.id)

        if category is None:
            raise CategoryNotFound("Category with id = {request.id} not found")

        return self.Output(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
