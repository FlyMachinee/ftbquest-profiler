from .lang_tree_node import LangTreeNode
import os
import json


class LangTree:
    def __init__(self, lang_code: str) -> None:
        if not isinstance(lang_code, str):
            raise TypeError("lang_code must be a string")
        if not lang_code:
            raise ValueError("lang_code cannot be empty")
        self.lang_code = lang_code
        self.root = LangTreeNode(children={})

    def insert(self, key: str, value: str) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        if not isinstance(value, str):
            raise TypeError("value must be a string")
        self.root.get_node(key, create=True).value = value

    def at(self, key: str) -> str | None:
        return self.root.get_node(key).value

    def contains(self, key: str) -> bool:
        self.root.contains(key)

    def from_lang_file(
        self, lang_dir: str, namespace: str | None = "ftbquests"
    ) -> None:
        file_path = os.path.join(lang_dir, f"{self.lang_code}.json")
        with open(file_path, "r", encoding="utf-8") as f:
            lang_data = json.load(f)
        if not isinstance(lang_data, dict):
            raise ValueError(
                f"Language file {file_path} does not contain a valid JSON object"
            )
        for key, value in lang_data.items():
            if not isinstance(value, str):
                raise ValueError(
                    f"Value for key '{key}' in language file {file_path} is not a string"
                )
            if not namespace:
                self.insert(key, value)
            elif key.startswith(f"{namespace}."):
                self.insert(key[len(namespace) + 1 :], value)

    def to_lang_file(
        self,
        lang_dir: str,
        namespace: str | None = "ftbquests",
        sort: bool = True,
    ) -> None:
        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)
        file_path = os.path.join(lang_dir, f"{self.lang_code}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("{\n")
            for key, value in self.root.walk(sort=sort):
                if namespace:
                    full_key = f"{namespace}.{key}"
                else:
                    full_key = key
                value_escaped = value.translate(
                    str.maketrans(
                        {
                            '"': r"\"",
                            "\n": r"\n",
                            "\r": r"\r",
                            "\t": r"\t",
                        }
                    )
                )
                f.write(f'  "{full_key}": "{value_escaped}",\n')
            # remove the last comma
            f.seek(f.tell() - 3)
            f.write("\n}\n")

    def get_lang_code(self) -> str:
        return self.lang_code

    def set_lang_code(self, lang_code: str) -> None:
        if not isinstance(lang_code, str):
            raise TypeError("lang_code must be a string")
        if not lang_code:
            raise ValueError("lang_code cannot be empty")
        self.lang_code = lang_code

    def get_node(self, key: str, create: bool = False) -> LangTreeNode:
        if create:
            return self.root.get_node(key, create=True)

        try:
            return self.root.get_node(key, create=False)
        except KeyError as e:
            raise KeyError(f"Key '{key}' not found in LangTree") from e

    def set_node(self, key: str, value: LangTreeNode) -> None:
        self.root.set_node(key, value)
