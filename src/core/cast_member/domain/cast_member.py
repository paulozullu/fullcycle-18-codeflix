from dataclasses import dataclass, field
from enum import StrEnum
import uuid
from uuid import UUID


class Type(StrEnum):
    ACTOR = "actor"
    DIRECTOR = "director"


@dataclass
class CastMember:
    id: UUID = field(default_factory=uuid.uuid4)
    name: str
    type: Type

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255")

        if not self.name:
            raise ValueError("name cannot be empty")

        if not self.type:
            raise ValueError("type cannot be empty")

        if not isinstance(self.type, Type):
            raise ValueError("invalid type")

    def __str__(self):
        return f"{self.name} - {self.type}"

    def __repr__(self):
        return f"<Cast Member {self.name} ({self.type})>"

    def __eq__(self, other):  # a == b -> a.__eq__(b)
        if not isinstance(other, CastMember):
            return False

        return self.id == other.id

    def update_cast_member(self, name, type):
        self.name = name
        self.type = type

        self.validate()
