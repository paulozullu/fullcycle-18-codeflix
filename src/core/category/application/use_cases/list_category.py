from dataclasses import dataclass
from uuid import UUID

from src.config import DEFAULT_PAGINATION_SIZE
from src.core._shared.list_use_case import ListOutputMeta, ListRequest, ListResponse
from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class ListCategoriesRequest(ListRequest): ...


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


@dataclass
class ListCategoryResponse(ListResponse):
    data: list[CategoryOutput]


class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: ListCategoriesRequest) -> ListCategoryResponse:
        categories = self.repository.find_all()
        sorted_categories = sorted(
            [
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in categories
            ],
            key=lambda category: getattr(category, request.order_by),
        )

        page_offset = (request.current_page - 1) * DEFAULT_PAGINATION_SIZE
        categories_page = sorted_categories[
            page_offset : page_offset + DEFAULT_PAGINATION_SIZE
        ]

        return ListCategoryResponse(
            data=categories_page,
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=DEFAULT_PAGINATION_SIZE,
                total=len(sorted_categories),
            ),
        )
