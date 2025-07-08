from dataclasses import dataclass

from src.core._shared.entity import BaseEntity


@dataclass
class Category(BaseEntity):
    name: str
    description: str = ""
    is_active: bool = True

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            # raise ValueError("name should not be longer than 255 characters")
            self.notification.add_error("name cannot be longer than 255")

        if not self.name:
            # raise ValueError("name should not be empty")
            self.notification.add_error("name cannot be empty")

        if len(self.description) > 1024:
            self.notification.add_error("description cannot be longer than 1024")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def __str__(self):
        return f"{self.name} - {self.description} ({self.is_active})"

    def __repr__(self):
        return f"{self.name} ({self.id})"

    def update_category(self, name, description):
        self.name = name
        self.description = description

        self.validate()

    def activate(self):
        self.is_active = True

        self.validate()

    def deactivate(self):
        self.is_active = False

        self.validate()
