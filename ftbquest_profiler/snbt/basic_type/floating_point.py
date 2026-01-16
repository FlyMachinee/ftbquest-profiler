# floating point types
class FloatingPoint(float):
    pass


# single precision floating point
class Float(FloatingPoint):
    def __repr__(self) -> str:
        return f"{float(self)}f"

    def __str__(self) -> str:
        return f"{float(self)}f"


# double precision floating point
class Double(FloatingPoint):
    def __repr__(self) -> str:
        return f"{float(self)}d"

    def __str__(self) -> str:
        return f"{float(self)}d"
