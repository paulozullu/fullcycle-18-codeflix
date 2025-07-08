from dataclasses import dataclass


@dataclass
class Notification:
    def __init__(self) -> None:
        self._errors: list[str] = []

    def add_error(self, error_message: str) -> None:
        self._errors.append(error_message)

    @property
    def has_errors(self) -> bool:
        return bool(self._errors)

    @property
    def messages(self) -> str:
        return ", ".join(self._errors)