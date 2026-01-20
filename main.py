from ftbquest_profiler import FTBQuestProfiler
from configparser import ConfigParser


def main() -> None:
    conf = ConfigParser()
    conf.read("config.ini", encoding="utf-8")
    profiler = FTBQuestProfiler(
        in_ftbq_dir=conf.get("ftbquests", "input_directory", fallback=""),
        out_ftbq_dir=conf.get("ftbquests", "output_directory", fallback=""),
        default_lang=conf.get("ftbquests", "language", fallback=""),
        in_lang_dir=conf.get("lang", "input_directory", fallback=""),
        out_lang_dir=conf.get("lang", "output_directory", fallback=""),
        out_namespace=conf.get("lang", "output_namespace", fallback=""),
        sort_lang=conf.getboolean("lang", "sort", fallback=True),
        logging=conf.getboolean("general", "logging", fallback=True),
        merge_raw_text=conf.getboolean(
            "ftbquests", "merge_raw_text", fallback=True
        ),
    )
    profiler.profile()


if __name__ == "__main__":
    main()
