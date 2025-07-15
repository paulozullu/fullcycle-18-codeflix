from abc import ABC
from dataclasses import dataclass, field

from src.config import DEFAULT_PAGINATION_SIZE

@dataclass
class ListRequest(ABC):
    current_page: int = 1
    order_by: str = "name"
    per_page: int = DEFAULT_PAGINATION_SIZE


@dataclass
class ListOutputMeta:
    total: int
    current_page: int = 1
    per_page: int = DEFAULT_PAGINATION_SIZE


@dataclass
class ListResponse(ABC):
    data: list[object]
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)
