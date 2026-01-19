from .lang_tree import LangTree
import os


class LangForest:
    def __init__(self) -> None:
        self.trees: dict[str, LangTree] = {}

    def __getitem__(self, lang_code: str) -> LangTree:
        return self.trees[lang_code]

    def __setitem__(self, lang_code: str, tree: LangTree) -> None:
        self.trees[lang_code] = tree

    def contains(self, lang_code: str) -> bool:
        return lang_code in self.trees

    def from_lang_dir(
        self, lang_dir: str, namespace: str | None = "ftbquests"
    ) -> None:
        for file_name in os.listdir(lang_dir):
            if file_name.endswith(".json"):
                lang_code = file_name[:-5]
                tree = LangTree(lang_code)
                tree.from_lang_file(lang_dir, namespace)
                self.trees[lang_code] = tree

    def to_lang_dir(
        self, lang_dir: str, namespace: str | None = "ftbquests"
    ) -> None:
        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)
        for tree in self.trees.values():
            tree.to_lang_file(lang_dir, namespace)
