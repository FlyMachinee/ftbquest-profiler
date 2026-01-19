from .lang_forest import *
from .snbt_parser import SNBTParser
from .snbt import SNBT, SNBTList
from .snbt.basic_type import *
import os
import json


class FTBQuestProfiler:
    def __init__(
        self,
        in_ftbq_dir: str,
        out_ftbq_dir: str,
        out_lang_dir: str,
        in_lang_dir: str = "",
        default_lang: str = "zh_cn",
        in_namespace: str = "ftbquests",
        out_namespace: str = "ftbquests",
        sort_lang: bool = False,
        logging: bool = True,
    ) -> None:
        self.logging = logging

        if not in_ftbq_dir:
            raise ValueError("Input FTBQuests directory is required.")
        if not os.path.exists(in_ftbq_dir):
            raise FileNotFoundError(
                f"Input FTBQuests directory '{in_ftbq_dir}' does not exist."
            )
        self.in_ftbq_dir = os.path.abspath(in_ftbq_dir)
        self.log(f"Input FTBQuests directory: {self.in_ftbq_dir}")

        if not out_ftbq_dir:
            raise ValueError("Output FTBQuests directory is required.")
        if not os.path.exists(out_ftbq_dir):
            os.makedirs(out_ftbq_dir)
        self.out_ftbq_dir = os.path.abspath(out_ftbq_dir)
        self.log(f"Output FTBQuests directory: {self.out_ftbq_dir}")

        if not default_lang:
            default_lang = "zh_cn"
            self.log("Quest language not specified. Using 'zh_cn'.")
        else:
            self.log(f"Quest language: {default_lang}")
        self.default_lang = default_lang

        if not in_lang_dir:
            self.in_lang_dir = ""
            self.log("Input language directory: (none)")
        else:
            if not os.path.exists(in_lang_dir):
                raise FileNotFoundError(
                    f"Input language directory '{in_lang_dir}' does not exist."
                )
            self.in_lang_dir = os.path.abspath(in_lang_dir)
            self.log(f"Input language directory: {self.in_lang_dir}")

        if not in_namespace:
            in_namespace = "ftbquests"
            self.log(
                "Input localization key prefix not specified. Using 'ftbquests'."
            )
        else:
            self.log(f"Input localization key prefix: {in_namespace}")
        self.in_namespace = in_namespace

        if not out_lang_dir:
            raise ValueError("Output language directory is required.")
        if not os.path.exists(out_lang_dir):
            os.makedirs(out_lang_dir)
        self.out_lang_dir = os.path.abspath(out_lang_dir)
        self.log(f"Output language directory: {self.out_lang_dir}")

        if not out_namespace:
            out_namespace = "ftbquests"
            self.log(
                "Output localization key prefix not specified. Using 'ftbquests'."
            )
        else:
            self.log(f"Output localization key prefix: {out_namespace}")
        self.out_namespace = out_namespace

        self.parser = SNBTParser()
        self.sort_lang = sort_lang

        self.log("FTBQuestProfiler initialized successfully.")

    def log(self, message: str) -> None:
        if self.logging:
            print("[INFO]", message)

    def warn(self, message: str) -> None:
        if self.logging:
            print("[WARN]", message)

    def error(self, message: str) -> None:
        if self.logging:
            print("[ERROR]", message)

    def profile(self) -> None:
        if self.in_lang_dir:
            self.lang_forest = LangForest()
            self.lang_forest.from_lang_dir(self.in_lang_dir, self.in_namespace)
        # Ensure default language tree exists
        if not self.lang_forest.contains(self.default_lang):
            self.lang_forest[self.default_lang] = LangTree(self.default_lang)

        self.do_data()
        self.do_chapter_groups()
        self.do_reward_tables()
        self.do_chapters()

        self.lang_forest.to_lang_dir(
            self.out_lang_dir, self.out_namespace, sort=self.sort_lang
        )
        self.log("FTBQuests profiling completed.")

    def do_chapters(self) -> None:
        pass

    def do_reward_tables(self) -> None:
        dir_name = "reward_tables"
        dir_path = os.path.join(self.in_ftbq_dir, dir_name)
        if not os.path.exists(dir_path):
            self.warn(
                f"'{dir_name}' directory not found in FTBQuests directory. Skipping."
            )
            return

        # iter all .snbt files in the reward_tables directory
        for file_name in os.listdir(dir_path):
            if not file_name.endswith(".snbt"):
                continue

            file_path = os.path.join(dir_path, file_name)
            try:
                snbt_obj = self.file_to_snbt(file_path)
            except Exception:
                continue

            if "title" not in snbt_obj:
                self.info(
                    f"Reward table '{file_name}' does not have a title. Skipping."
                )
                continue

            # translate the title
            title_string = snbt_obj["title"]
            if not isinstance(title_string, String):
                self.warn(
                    f"Reward table '{file_name}' title is not a string. Skipping."
                )
                continue

            if not title_string:
                # skip empty title
                continue

            # test if is a localization key
            if self.process_if_localization_key(title_string, file_name):
                continue

            # no, process as raw text
            # generate a new localization key
            key = f"reward_{file_name[:-5]}.title"
            # insert into all lang trees
            for tree in self.lang_forest.trees.values():
                tree.insert(key, title_string)
            # modify the snbt object
            snbt_obj["title"] = String(f"{{{self.out_namespace}.{key}}}")
            # write back to output directory
            out_file_dir_path = os.path.join(self.out_ftbq_dir, dir_name)
            if not os.path.exists(out_file_dir_path):
                os.makedirs(out_file_dir_path)
            out_file_path = os.path.join(self.out_ftbq_dir, dir_name, file_name)
            with open(out_file_path, "w", encoding="utf-8") as dst:
                snbt_obj.pretty_file(dst)
            # done

    def do_chapter_groups(self) -> None:
        file_name = "chapter_groups.snbt"
        file_path = os.path.join(self.in_ftbq_dir, file_name)
        if not os.path.exists(file_path):
            self.warn(
                f"'{file_name}' not found in FTBQuests directory. Skipping."
            )
            return

        try:
            snbt_obj = self.file_to_snbt(file_path)
        except Exception:
            return

        if not "chapter_groups" in snbt_obj:
            self.error(
                f"'{file_name}' does not contain 'chapter_groups' key. Skipping."
            )
            return

        groups = snbt_obj["chapter_groups"]
        if not isinstance(groups, SNBTList):
            self.error(
                f"'chapter_groups' in '{file_name}' is not a list. Skipping."
            )
            return

        for elem in groups:
            if not isinstance(elem, SNBT):
                self.warn(
                    f"An element '{elem}' in 'chapter_groups' is not a compound. Skipping."
                )
                continue

            if "id" not in elem:
                self.error(
                    f"An compound '{elem}' in 'chapter_groups' does not have 'id'. Skipping."
                )
                continue
            groups_id = elem["id"]
            if not isinstance(groups_id, String):
                self.error(
                    f"Chapter group id '{groups_id}' is not a string. Skipping."
                )
                continue

            if "title" not in elem:
                self.error(
                    f"Chapter group '{groups_id}' does not have a 'title' key. Skipping."
                )
                continue
            groups_title = elem["title"]
            if not isinstance(groups_title, String):
                self.error(
                    f"Chapter group '{groups_id}' title is not a string. Skipping."
                )
                continue

            # test if is a localization key
            if self.process_if_localization_key(
                groups_title, f"{file_name} (group {groups_id})"
            ):
                continue

            # no, process as raw text
            # generate a new localization key
            key = f"group_{groups_id.raw()}.title"
            # insert into all lang trees
            for tree in self.lang_forest.trees.values():
                tree.insert(key, groups_title)
            # modify the snbt object
            elem["title"] = String(f"{{{self.out_namespace}.{key}}}")
            # done in this group

        # after all groups processed, write back to output directory
        out_file_path = os.path.join(self.out_ftbq_dir, file_name)
        with open(out_file_path, "w", encoding="utf-8") as dst:
            snbt_obj.pretty_file(dst)
        # done

    def do_data(self) -> None:
        file_name = "data.snbt"
        file_path = os.path.join(self.in_ftbq_dir, file_name)

        if not os.path.exists(file_path):
            self.warn(
                f"'{file_name}' not found in FTBQuests directory. Skipping."
            )
            return

        try:
            snbt_obj = self.file_to_snbt(file_path)
        except Exception:
            return

        keys_needed = []

        if "title" in snbt_obj:
            keys_needed.append("title")
        else:
            self.error(f"'{file_name}' does not contain 'title' key. Skipping.")
        if "lock_message" in snbt_obj:
            keys_needed.append("lock_message")
        else:
            self.error(
                f"'{file_name}' does not contain 'lock_message' key. Skipping."
            )

        for key in keys_needed:
            value = snbt_obj[key]
            if not isinstance(value, String):
                self.error(
                    f"'{key}' in '{file_name}' is not a string. Skipping."
                )
                continue

            if not value:
                # skip empty string
                continue

            # test if is a localization key
            if self.process_if_localization_key(value, f"{file_name} ({key})"):
                continue

            # no, process as raw text
            # generate a new localization key
            new_key = f"data.{key}"
            # insert into all lang trees
            for tree in self.lang_forest.trees.values():
                tree.insert(new_key, value)
            # modify the snbt object
            snbt_obj[key] = String(f"{{{self.out_namespace}.{new_key}}}")
            # done in this key

        # after all keys processed, write back to output directory
        out_file_path = os.path.join(self.out_ftbq_dir, file_name)
        with open(out_file_path, "w", encoding="utf-8") as dst:
            snbt_obj.pretty_file(dst)

    def file_to_snbt(self, file_path: str) -> SNBT:
        with open(file_path, "r", encoding="utf-8") as src:
            try:
                snbt_obj = self.parser.parse_file(src)
            except Exception as e:
                self.error(f"Failed to parse SNBT file '{file_path}': {e}.")
                self.parser.restart()
                raise e
        return snbt_obj

    def process_if_localization_key(
        self, string: String, file_name: str
    ) -> bool:
        if string[0] == "{" and string[-1] == "}":
            # looks like a localization key
            key = string[1:-1]
            if key.startswith(self.in_namespace + "."):
                # extract the actual key
                key = key[len(self.in_namespace) + 1 :]

                default_tree = self.lang_forest[self.default_lang]
                # check if the key is in the default lang tree
                if default_tree.contains(key):
                    # yes, try copy value to other lang tree if not exist
                    for (
                        lang,
                        tree,
                    ) in self.lang_forest.trees.items():
                        if lang == self.default_lang:
                            continue
                        if not tree.contains(key):
                            tree.insert(key, default_tree.at(key))
                    # all done in this file
                    return True
                else:
                    # no, serve as raw string and warn
                    self.warn(
                        f"Localization key '{self.in_namespace}.{key}' in file '{file_name}' not found in '{self.default_lang}.json' lang file. Serving as raw text."
                    )
            else:
                self.warn(
                    f"Localization key '{key}' in file '{file_name}' does not start with prefix '{self.in_namespace}'. Serving as raw text."
                )
        return False
