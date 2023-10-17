import json
import os

locales = {}
for locale_file_name in os.listdir("bot/locales"):
    with open(
        os.path.join("bot/locales", locale_file_name), "r+", encoding="utf-8"
    ) as locale_file:
        locales[locale_file_name.split(".")[0]] = json.load(locale_file)


def get_text(title: str, lang: str = "ru") -> str:
    return locales[lang][title]
