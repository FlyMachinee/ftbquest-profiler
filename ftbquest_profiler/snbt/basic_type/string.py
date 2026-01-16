class String(str):
    def __str__(self) -> str:
        escaped = self.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
