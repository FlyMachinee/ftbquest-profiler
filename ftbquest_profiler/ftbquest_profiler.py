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
        self.get_langs()
        self.out_langs: dict[str, dict[str, str]] = dict()
        for lang_code in self.in_langs:
            self.out_langs[lang_code] = dict()
        self.do_data()
        self.do_chapter_groups()
        self.do_reward_tables()
        self.do_chapters()
        self.save_langs()
        self.log("FTBQuests profiling completed.")

    def get_langs(self):
        langs: dict[str, dict[str, str]] = dict()
        if self.in_lang_dir:
            for file_name in os.listdir(self.in_lang_dir):
                if not file_name.endswith(".json"):
                    self.warn(
                        f"Non-JSON file '{file_name}' found in lang/. Skipping."
                    )
                    continue

                lang_code = file_name[:-5]
                file_path = os.path.join(self.in_lang_dir, file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        lang_data = json.load(f)
                    except Exception as e:
                        self.error(
                            f"Failed to parse language file '{file_path}': {e}."
                        )
                        continue
                if not isinstance(lang_data, dict):
                    self.error(
                        f"Language file '{file_path}' does not contain a valid JSON object. Skipping."
                    )
                    continue
                lang: dict[str, str] = dict()
                for k, v in lang_data.items():
                    if not isinstance(v, str):
                        self.error(
                            f"Value for key '{k}' in language file '{file_path}' is not a string. Skipping."
                        )
                    else:
                        lang[k] = v
                langs[lang_code] = lang
        if self.default_lang not in langs:
            langs[self.default_lang] = dict()
        self.in_langs = langs

    def save_langs(self) -> None:
        langs = self.out_langs
        for lang_code, lang_data in langs.items():
            file_path = os.path.join(self.out_lang_dir, f"{lang_code}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(
                    lang_data,
                    f,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=self.sort_lang,
                )

    def do_chapters(self) -> None:
        dir_name = "chapters"
        dir_path = os.path.join(self.in_ftbq_dir, dir_name)
        if not os.path.exists(dir_path):
            self.warn(
                f"'{dir_name}' directory not found in FTBQuests directory. Skipping."
            )
            return

        # iter all .snbt files in the chapters directory
        for file_name in os.listdir(dir_path):
            if not file_name.endswith(".snbt"):
                self.warn(
                    f"Non-snbt file '{file_name}' found in chapters/. Skipping."
                )
                continue

            file_path = os.path.join(dir_path, file_name)
            try:
                snbt_obj = self.file_to_snbt(file_path)
            except Exception:
                continue

            self.do_chapter(file_name, snbt_obj)

            # write back to output directory
            out_file_dir_path = os.path.join(self.out_ftbq_dir, dir_name)
            if not os.path.exists(out_file_dir_path):
                os.makedirs(out_file_dir_path)
            out_file_path = os.path.join(self.out_ftbq_dir, dir_name, file_name)
            with open(out_file_path, "w", encoding="utf-8") as dst:
                snbt_obj.pretty_file(dst)

    def do_chapter(self, file_name: str, chapter: SNBT) -> None:
        # handle chapter title
        if "title" in chapter:
            chapter_title = chapter["title"]
            if not isinstance(chapter_title, String):
                self.error(
                    f"Chapter '{file_name}' title is not a string. Skipping."
                )
                return

            if chapter_title:
                new_key = f"{self.out_namespace}.chapter_{file_name[:-5]}.title"
                self.update_out_langs(chapter_title.raw(), file_name, new_key)

                # modify the snbt object
                chapter["title"] = String(f"{{{new_key}}}")
                # done in chapter title

        # handle subtitles
        if "subtitle" in chapter:
            chapter_subtitles = chapter["subtitle"]
            if not isinstance(chapter_subtitles, SNBTList):
                self.error(
                    f"Chapter '{file_name}' subtitle is not a list. Skipping."
                )
                return
            for i, chapter_subtitle in enumerate(chapter_subtitles):
                if not isinstance(chapter_subtitle, String):
                    self.error(
                        f"Chapter '{file_name}' subtitle index {i} is not a string. Skipping."
                    )
                    continue

                if not chapter_subtitle:
                    # skip empty subtitle
                    continue

                new_key = f"{self.out_namespace}.chapter_{file_name[:-5]}.subtitle_{i+1}"
                self.update_out_langs(
                    chapter_subtitle.raw(), file_name, new_key
                )

                # modify the snbt object
                chapter_subtitles[i] = String(f"{{{new_key}}}")
                # done in this subtitle

        # handle quests
        if "quests" in chapter:
            quests = chapter["quests"]
            if not isinstance(quests, SNBTList):
                self.error(
                    f"Chapter '{file_name}' quests is not a list. Skipping."
                )
                return
            for quest in quests:
                if not isinstance(quest, SNBT):
                    self.warn(
                        f"An element '{quest}' in chapter '{file_name}' quests is not a compound. Skipping."
                    )
                    continue
                self.do_quest(file_name, quest)

    def do_quest(self, file_name: str, quest: SNBT) -> None:
        # get id
        if "id" not in quest:
            self.error(
                f"A quest '{quest}' in chapter '{file_name}' does not have 'id'. Skipping."
            )
            return
        quest_id = quest["id"]
        if not isinstance(quest_id, String):
            self.error(
                f"Quest id '{quest_id}' in chapter '{file_name}' is not a string. Skipping."
            )
            return

        # handle quest title and subtitle
        for key in ["title", "subtitle"]:
            if key in quest:
                value = quest[key]
                if not isinstance(value, String):
                    self.error(
                        f"Quest '{quest_id.raw()}' {key} in chapter '{file_name}' is not a string. Skipping."
                    )
                    continue

                if not value:
                    # skip empty string
                    continue

                new_key = f"{self.out_namespace}.chapter_{file_name[:-5]}.quest_{quest_id.raw()}.{key}"
                self.update_out_langs(value.raw(), file_name, new_key)

                # modify the snbt object
                quest[key] = String(f"{{{new_key}}}")
                # done in this key

        # handle tasks and rewards title
        for key in ["tasks", "rewards"]:
            if key in quest:
                items = quest[key]
                if not isinstance(items, SNBTList):
                    self.error(
                        f"Quest '{quest_id.raw()}' {key} in chapter '{file_name}' is not a list. Skipping."
                    )
                    continue
                for item in items:
                    if not isinstance(item, SNBT):
                        self.warn(
                            f"An element '{item}' in quest '{quest_id.raw()}' {key} in chapter '{file_name}' is not a compound. Skipping."
                        )
                        continue

                    # get id
                    if "id" not in item:
                        self.error(
                            f"An item '{item}' in quest '{quest_id.raw()}' {key} in chapter '{file_name}' does not have 'id'. Skipping."
                        )
                        continue
                    item_id = item["id"]
                    if not isinstance(item_id, String):
                        self.error(
                            f"An item id '{item_id}' in quest '{quest_id.raw()}' {key} in chapter '{file_name}' is not a string. Skipping."
                        )
                        continue

                    if "title" in item:
                        item_title = item["title"]
                        if not isinstance(item_title, String):
                            self.error(
                                f"Item '{item_id.raw()}' title in quest '{quest_id.raw()}' {key} in chapter '{file_name}' is not a string. Skipping."
                            )
                            continue

                        if not item_title:
                            # skip empty title
                            continue

                        new_key = f"{self.out_namespace}.chapter_{file_name[:-5]}.quest_{quest_id.raw()}.{key[:-1]}_{item_id.raw()}.title"
                        self.update_out_langs(
                            item_title.raw(), file_name, new_key
                        )

                        # modify the snbt object
                        item["title"] = String(f"{{{new_key}}}")
                        # done in this item title

        # handle quest description
        if "description" not in quest:
            return

        descriptions = quest["description"]
        if not isinstance(descriptions, SNBTList):
            self.error(
                f"Quest '{quest_id.raw()}' description in chapter '{file_name}' is not a list. Skipping."
            )
            return

        counter = 1
        for i, desc in enumerate(descriptions):
            if not isinstance(desc, String):
                self.error(
                    f"A description entry '{desc}' in quest '{quest_id.raw()}' in chapter '{file_name}' is not a string. Skipping."
                )
                continue

            if not desc or desc == "{@pagebreak}":
                # skip empty description or pagebreak
                continue

            raw_desc = desc.raw()

            try:
                decoded_desc = (
                    raw_desc.replace("\\n", "\n")
                    .replace("\\r", "\r")
                    .replace("\\t", "\t")
                    .replace('\\"', '"')
                    .replace("\\\\", "\\")
                )
                json_obj = json.loads(decoded_desc)
                is_json = True
            except Exception:
                # not a json
                json_obj = None
                is_json = False

            if not is_json:
                new_key = f"{self.out_namespace}.chapter_{file_name[:-5]}.quest_{quest_id.raw()}.desc_{counter:02d}"
                self.update_out_langs(raw_desc, file_name, new_key)

                # modify the snbt object
                descriptions[i] = String(f"{{{new_key}}}")
                # done in this description
                counter += 1
                continue

            # is a json object
            if not json_obj:
                # empty json object
                continue

            def do_json_text(json_obj: dict, rich_num: int) -> bool:
                if "translate" in json_obj:
                    rich_text = json_obj["translate"]
                    if not isinstance(rich_text, str):
                        self.error(
                            f"The 'translate' field in description entry '{desc.raw()}' in quest '{quest_id.raw()}' in chapter '{file_name}' is not a string. Skipping."
                        )
                        return False
                    # assume it's a key
                    rich_text = f"{{{rich_text}}}"
                elif "text" not in json_obj:
                    self.warn(
                        f"A description entry '{desc.raw()}' in quest '{quest_id.raw()}' in chapter '{file_name}' JSON object does not contain 'text'. Skipping."
                    )
                    return False
                else:
                    rich_text = json_obj["text"]
                    if not isinstance(rich_text, str):
                        self.error(
                            f"The 'text' / 'translate' field in description entry '{desc.raw()}' in quest '{quest_id.raw()}' in chapter '{file_name}' is not a string. Skipping."
                        )
                        return False

                if not rich_text:
                    # skip empty text
                    return False

                new_key = f"{self.out_namespace}.chapter_{file_name[:-5]}.quest_{quest_id.raw()}.desc_{counter:02d}.rich_{rich_num:02d}"
                self.update_out_langs(rich_text, file_name, new_key)
                if "text" in json_obj:
                    del json_obj["text"]
                json_obj["translate"] = new_key
                return True

            success = False
            if isinstance(json_obj, dict):
                if do_json_text(json_obj, 1):
                    success = True
            elif isinstance(json_obj, list):
                rich_num = 1
                for j, elem in enumerate(json_obj):
                    if isinstance(elem, dict):
                        if do_json_text(elem, rich_num):
                            rich_num += 1
                            success = True
                    elif isinstance(elem, str):
                        # raw text in array
                        if not elem:
                            continue

                        new_key = f"{self.out_namespace}.chapter_{file_name[:-5]}.quest_{quest_id.raw()}.desc_{counter:02d}.rich_{rich_num:02d}"
                        self.update_out_langs(elem, file_name, new_key)
                        json_obj[j] = {"translate": new_key}
                        rich_num += 1
                        success = True
                if not isinstance(json_obj[0], str):
                    # insert an empty string at the beginning to avoid issues
                    json_obj.insert(0, "")
            else:
                self.error("Control flow should not reach here.")
                continue

            if success:
                # modify the snbt object
                new_desc_str = json.dumps(json_obj, ensure_ascii=False)
                descriptions[i] = String(new_desc_str)
                # done in this description
                counter += 1
                continue

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
                self.warn(
                    f"Non-snbt file '{file_name}' found in reward_tables/. Skipping."
                )
                continue

            file_path = os.path.join(dir_path, file_name)
            try:
                snbt_obj = self.file_to_snbt(file_path)
            except Exception:
                continue

            if "title" not in snbt_obj:
                continue

            # translate the title
            title_string = snbt_obj["title"]
            if not isinstance(title_string, String):
                self.error(
                    f"Reward table '{file_name}' title is not a string. Skipping."
                )
                continue

            if not title_string:
                # skip empty title
                continue

            key = f"{self.out_namespace}.reward_{file_name[:-5]}.title"
            self.update_out_langs(title_string.raw(), file_name, key)

            # modify the snbt object
            snbt_obj["title"] = String(f"{{{key}}}")
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
                continue
            groups_title = elem["title"]
            if not isinstance(groups_title, String):
                self.error(
                    f"Chapter group '{groups_id}' title is not a string. Skipping."
                )
                continue

            if not groups_title:
                # skip empty title
                continue

            new_key = f"{self.out_namespace}.group_{groups_id.raw()}.title"
            self.update_out_langs(groups_title.raw(), file_name, new_key)

            # modify the snbt object
            elem["title"] = String(f"{{{new_key}}}")
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

        for key in ["title", "lock_message"]:
            if key in snbt_obj:
                value = snbt_obj[key]
                if not isinstance(value, String):
                    self.error(
                        f"'{key}' in '{file_name}' is not a string. Skipping."
                    )
                    continue

                if not value:
                    # skip empty string
                    continue

                new_key = f"{self.out_namespace}.data.{key}"
                self.update_out_langs(value.raw(), file_name, new_key)

                # modify the snbt object
                snbt_obj[key] = String(f"{{{new_key}}}")
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

    def update_out_langs(
        self, str_or_key: str, file_name: str, new_key: str
    ) -> None:
        if not str_or_key:
            return
        if str_or_key[0] == "{" and str_or_key[-1] == "}":
            # looks like a key
            key = str_or_key[1:-1]
            if key in self.in_langs[self.default_lang]:
                value = self.in_langs[self.default_lang][key]
            else:
                # not found, warn and serve as raw text
                self.warn(
                    f"Localization key '{key}' in file '{file_name}' not found in '{self.default_lang}.json' lang file. Serving as raw text."
                )
                value = str_or_key
            # insert into out_langs
            for lang_code in self.out_langs:
                if key in self.in_langs[lang_code]:
                    self.out_langs[lang_code][new_key] = self.in_langs[
                        lang_code
                    ][key]
                else:
                    self.out_langs[lang_code][new_key] = value
        else:
            # raw text
            value = str_or_key
            for lang_code in self.out_langs:
                self.out_langs[lang_code][new_key] = value
