from abc import ABC
from dataclasses import dataclass, field

PER_PAGE_DEFAULT = 2


@dataclass
class ListRequest(ABC):
    current_page: int = 1
    order_by: str = "name"
    per_page: int = PER_PAGE_DEFAULT


@dataclass
class ListOutputMeta:
    total: int
    current_page: int = 1
    per_page: int = PER_PAGE_DEFAULT


@dataclass
class ListResponse(ABC):
    data: list[object]
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)
