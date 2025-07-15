from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from src.config import DEFAULT_PAGINATION_SIZE


@dataclass
class ListInput(ABC):
    current_page: int = 1
    order_by: str = "name"
    per_page: int = DEFAULT_PAGINATION_SIZE


@dataclass
class ListOutputMeta:
    total: int = 0
    current_page: int = 1
    per_page: int = DEFAULT_PAGINATION_SIZE


T = TypeVar("T")


@dataclass
class ListOutput(Generic[T], ABC):
    data: list[T] = field(default_factory=list)
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)
