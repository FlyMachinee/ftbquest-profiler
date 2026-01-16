from typing import Literal


class Boolean:
    def __init__(self, value) -> None:
        self.value = bool(value)

    def __bool__(self) -> bool:
        return self.value

    def __str__(self) -> Literal["true"] | Literal["false"]:
        return "true" if self.value else "false"
