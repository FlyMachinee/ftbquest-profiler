from typing import Literal


class Boolean:
    def __init__(self, value) -> None:
        self.value = bool(value)

    def __bool__(self) -> bool:
        return self.value

    def __str__(self) -> Literal["true"] | Literal["false"]:
        return "true" if self.value else "false"

    def __repr__(self) -> str:
        return f"Boolean({self.value})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Boolean):
            return self.value == other.value
        return False
