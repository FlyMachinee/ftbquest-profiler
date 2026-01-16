from __future__ import annotations
from io import FileIO, StringIO
from typing import Union
from .basic_type import *

SNBTValue = Union[
    "SNBT",
    Number,
    FloatingPoint,
    Boolean,
    String,
    "SNBTList",
]


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
        if not isinstance(file, FileIO):
            raise TypeError("file must be a FileIO instance")
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
        if not isinstance(stream, (FileIO, StringIO)):
            raise TypeError("stream must be a FileIO or StringIO instance")

        sep_start, sep_mid, sep_end = seps
        indent_str = indent * indent_level
        inner_indent_str = indent * (indent_level + 1)

        if not self:
            stream.write("[ ]")
            return

        if len(self) == 1:
            item = self[0]
            if isinstance(item, (SNBT, SNBTList)):
                item.pretty(
                    stream=stream,
                    seps=seps,
                    indent=indent,
                    indent_level=indent_level,
                )
            else:
                stream.write(f"[{str(item)}]")
            return

        stream.write("[")
        for i, item in enumerate(self):
            if i == 0:
                stream.write(sep_start + inner_indent_str)
            else:
                stream.write(sep_mid + inner_indent_str)
            if isinstance(item, (SNBT, SNBTList)):
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
        if not isinstance(file, FileIO):
            raise TypeError("file must be a FileIO instance")

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
        if not isinstance(stream, (FileIO, StringIO)):
            raise TypeError("stream must be a FileIO or StringIO instance")

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
            stream.write(f"{key}: ")
            if isinstance(value, (SNBT, SNBTList)):
                value.pretty(
                    stream=stream,
                    seps=seps,
                    indent=indent,
                    indent_level=indent_level + 1,
                )
            else:
                stream.write(str(value))
        stream.write(sep_end + indent_str + "}")
