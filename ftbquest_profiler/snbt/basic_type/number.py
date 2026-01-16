from typing import Self


# integer wrapper classes
class Number(int):
    pass


# byte integer (-128 to 127)
class Byte(Number):
    def __new__(cls, value) -> Self:
        if not (-128 <= value <= 127):
            raise ValueError("Byte value must be between -128 and 127")
        return super().__new__(cls, value)

    def __repr__(self) -> str:
        return f"{int(self)}b"

    def __str__(self) -> str:
        return f"{int(self)}b"


# short integer (-32,768 to 32,767)
class Short(Number):
    def __new__(cls, value) -> Self:
        if not (-32768 <= value <= 32767):
            raise ValueError("Short value must be between -32,768 and 32,767")
        return super().__new__(cls, value)

    def __repr__(self) -> str:
        return f"{int(self)}s"

    def __str__(self) -> str:
        return f"{int(self)}s"


# integer (-2,147,483,648 to 2,147,483,647)
class Int(Number):
    def __new__(cls, value) -> Self:
        if not (-2147483648 <= value <= 2147483647):
            raise ValueError(
                "Int value must be between -2,147,483,648 and 2,147,483,647"
            )
        return super().__new__(cls, value)

    def __repr__(self) -> str:
        return f"{int(self)}"

    def __str__(self) -> str:
        return f"{int(self)}"


# long integer (-9,223,372,036,854,775,808 to 9,223,372,036,854,775,807)
class Long(Number):
    def __new__(cls, value) -> Self:
        if not (-9223372036854775808 <= value <= 9223372036854775807):
            raise ValueError(
                "Long value must be between -9,223,372,036,854,775,808 and 9,223,372,036,854,775,807"
            )
        return super().__new__(cls, value)

    def __repr__(self) -> str:
        return f"{int(self)}l"

    def __str__(self) -> str:
        return f"{int(self)}l"
