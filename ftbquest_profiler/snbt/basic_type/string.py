class String(str):
    def __str__(self) -> str:
        return f'"{super().__str__()}"'

    def __repr__(self) -> str:
        return f"String({super().__repr__()})"

    def raw(self) -> str:
        return super().__str__()
