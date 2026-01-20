class String(str):
    def __str__(self) -> str:
        escaped = (
            super()
            .__str__()
            .replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\t", "\\t")
            .replace("\r", "\\r")
        )
        return f'"{escaped}"'

    def __repr__(self) -> str:
        return f"String({super().__repr__()})"

    def raw(self) -> str:
        return super().__str__()
