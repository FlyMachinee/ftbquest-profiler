from __future__ import annotations


class LangTreeNode:
    def __init__(
        self,
        value: str | None = None,
        children: dict[str, LangTreeNode] | None = None,
    ) -> None:
        self.value = value
        self.children = children

    def get_node(self, key_path: str, create: bool = False) -> LangTreeNode:
        if key_path.find(".") != -1:
            # allow nested access using dot notation like "ftbquests.chapterxxx.questxxxx.title"
            parts = key_path.split(".", 1)
            first_part = parts[0]
            rest_part = parts[1]
            if create:
                child_node = self.children.setdefault(
                    first_part, LangTreeNode(children={})
                )
                return child_node.get_node(rest_part, create=True)
            else:
                child_node = self.children.get(first_part)
                if not child_node:
                    raise KeyError(
                        f"Key '{first_part}' does not refer to a LangTreeNode, but None"
                    )
                return child_node.get_node(rest_part, create=False)
        else:
            if create:
                return self.children.setdefault(
                    key_path, LangTreeNode(children={})
                )
            else:
                child_node = self.children.get(key_path)
                if not child_node:
                    raise KeyError(
                        f"Key '{key_path}' does not refer to a LangTreeNode, but None"
                    )
                return child_node

    def set_node(self, key_path: str, value: LangTreeNode) -> None:
        if key_path.find(".") != -1:
            # allow nested access using dot notation like "ftbquests.chapterxxx.questxxxx.title"
            parts = key_path.split(".", 1)
            first_part = parts[0]
            rest_part = parts[1]
            child_node = self.children.setdefault(
                first_part, LangTreeNode(children={})
            )
            child_node.set_node(rest_part, value)
        else:
            self.children[key_path] = value

    def contains(self, key_path: str) -> bool:
        if key_path.find(".") != -1:
            parts = key_path.split(".", 1)
            first_part = parts[0]
            rest_part = parts[1]
            if first_part not in self.children:
                return False
            child_node = self.children[first_part]
            return child_node.contains(rest_part)
        else:
            return key_path in self.children

    def walk(self, prefix: str = ""):
        if self.value:
            yield prefix, self.value
        for key, value in self.children.items():
            full_key = f"{prefix}.{key}" if prefix else key
            yield from value.walk(full_key)
