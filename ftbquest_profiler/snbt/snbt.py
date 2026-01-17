from __future__ import annotations
from io import FileIO, StringIO
from typing import Union
import array as arr
from .basic_type import *

SNBTValue = Union[
    "SNBT",
    Number,
    "SNBTArray",
    FloatingPoint,
    Boolean,
    String,
    "SNBTList",
]


# allow Byte, Int, Long arrays in SNBT
class SNBTArray(arr.array):
    def pretty_str(
        self,
        seps: tuple[str, str, str] = ("\n", "\n", "\n"),
        indent: str = "\t",
        indent_level: int = 0,
    ) -> str:
        stream = StringIO()
        self.pretty(
            stream=stream,
            seps=seps,
            indent=indent,
            indent_level=indent_level,
        )
        return stream.getvalue()

    def pretty_file(
        self,
        file: FileIO,
        seps: tuple[str, str, str] = ("\n", "\n", "\n"),
        indent: str = "\t",
        indent_level: int = 0,
    ) -> None:
        self.pretty(
            stream=file,
            seps=seps,
            indent=indent,
            indent_level=indent_level,
        )

    def pretty(
        self,
        stream: Union[FileIO, StringIO],
        seps: tuple[str, str, str],
        indent: str,
        indent_level: int,
    ) -> None:
        sep_start, sep_mid, sep_end = seps
        indent_str = indent * indent_level
        inner_indent_str = indent * (indent_level + 1)

        if not self:
            stream.write(f"[{self.typecode.capitalize()}; ]")
            return

        stream.write(f"[{self.typecode.capitalize()};")
        for i, item in enumerate(self):
            if i == 0:
                stream.write(sep_start + inner_indent_str)
            else:
                stream.write(sep_mid + inner_indent_str)
            stream.write(str(item))
        stream.write(sep_end + indent_str + "]")


class SNBTList(list[SNBTValue]):
    def pretty_str(
        self,
        seps: tuple[str, str, str] = ("\n", "\n", "\n"),
        indent: str = "\t",
        indent_level: int = 0,
    ) -> str:
        stream = StringIO()
        self.pretty(
            stream=stream,
            seps=seps,
            indent=indent,
            indent_level=indent_level,
        )
        return stream.getvalue()

    def pretty_file(
        self,
        file: FileIO,
        seps: tuple[str, str, str] = ("\n", "\n", "\n"),
        indent: str = "\t",
        indent_level: int = 0,
    ) -> None:
        self.pretty(
            stream=file,
            seps=seps,
            indent=indent,
            indent_level=indent_level,
        )

    def pretty(
        self,
        stream: Union[FileIO, StringIO],
        seps: tuple[str, str, str],
        indent: str,
        indent_level: int,
    ) -> None:
        sep_start, sep_mid, sep_end = seps
        indent_str = indent * indent_level
        inner_indent_str = indent * (indent_level + 1)

        if not self:
            stream.write("[ ]")
            return

        if len(self) == 1:
            item = self[0]
            if isinstance(item, (SNBT, SNBTList, SNBTArray)):
                stream.write("[")
                item.pretty(
                    stream=stream,
                    seps=seps,
                    indent=indent,
                    indent_level=indent_level,
                )
                stream.write("]")
            else:
                stream.write(f"[{str(item)}]")
            return

        stream.write("[")
        for i, item in enumerate(self):
            if i == 0:
                stream.write(sep_start + inner_indent_str)
            else:
                stream.write(sep_mid + inner_indent_str)
            if isinstance(item, (SNBT, SNBTList, SNBTArray)):
                item.pretty(
                    stream=stream,
                    seps=seps,
                    indent=indent,
                    indent_level=indent_level + 1,
                )
            else:
                stream.write(str(item))
        stream.write(sep_end + indent_str + "]")


class SNBT(dict[str, SNBTValue]):
    def pretty_str(
        self,
        seps: tuple[str, str, str] = ("\n", "\n", "\n"),
        indent: str = "\t",
        indent_level: int = 0,
    ) -> str:
        stream = StringIO()
        self.pretty(
            stream=stream,
            seps=seps,
            indent=indent,
            indent_level=indent_level,
        )
        return stream.getvalue()

    def pretty_file(
        self,
        file: FileIO,
        seps: tuple[str, str, str] = ("\n", "\n", "\n"),
        indent: str = "\t",
        indent_level: int = 0,
    ) -> None:
        self.pretty(
            stream=file,
            seps=seps,
            indent=indent,
            indent_level=indent_level,
        )

    def pretty(
        self,
        stream: Union[FileIO, StringIO],
        seps: tuple[str, str, str],
        indent: str,
        indent_level: int,
    ) -> None:
        sep_start, sep_mid, sep_end = seps
        indent_str = indent * indent_level
        inner_indent_str = indent * (indent_level + 1)

        if not self:
            stream.write("{ }")
            return

        stream.write("{")
        for i, (key, value) in enumerate(self.items()):
            if i == 0:
                stream.write(sep_start + inner_indent_str)
            else:
                stream.write(sep_mid + inner_indent_str)

            if set(key) & set(":."):
                stream.write(f'"{key}": ')
            else:
                stream.write(f"{key}: ")

            if isinstance(value, SNBT):
                if key == "item" and not "tag" in value:
                    value.pretty(
                        stream=stream,
                        seps=(" ", ", ", " "),
                        indent="",
                        indent_level=0,
                    )
                else:
                    value.pretty(
                        stream=stream,
                        seps=seps,
                        indent=indent,
                        indent_level=indent_level + 1,
                    )
            elif isinstance(value, SNBTList):
                if indent_level == 0 and (
                    key == "chapter_groups" or key == "rewards"
                ):
                    stream.write("[")
                    for j, item in enumerate(value):
                        if j == 0:
                            stream.write(sep_start + inner_indent_str + indent)
                        else:
                            stream.write(sep_mid + inner_indent_str + indent)

                        assert isinstance(item, SNBT)
                        item.pretty(
                            stream=stream,
                            seps=(" ", ", ", " "),
                            indent="",
                            indent_level=0,
                        )
                    stream.write(sep_end + inner_indent_str + "]")
                else:
                    value.pretty(
                        stream=stream,
                        seps=seps,
                        indent=indent,
                        indent_level=indent_level + 1,
                    )
            elif isinstance(value, SNBTArray):
                value.pretty(
                    stream=stream,
                    seps=seps,
                    indent=indent,
                    indent_level=indent_level + 1,
                )
            else:
                stream.write(str(value))
        stream.write(sep_end + indent_str + "}")
