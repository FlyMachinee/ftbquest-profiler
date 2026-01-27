# FTBQuestProfiler

Other languages:
- [[Simplified Chinese / 简体中文 / zh_cn]](README_zh_cn.md)

## Usage

1. Clone this repo to your computer, checkout to `main` branch
2. Set up Python environment (3.12+ recommended), install packages in `requirements.txt`
3. Configure configurations in `config.ini`
4. Run `python ./main.py` in the repo directory
5. (go you)

## Functionality

`FTBQuestProfiler` can replace description texts with localization keys in `.snbt` files that FTBQuests mod (<= Minecraft 1.20) generated, and generate corresponding `.json` files for further translation. Support rich text, `JSON` objects (used in quest links).

### Fields Supported

- `chapter_groups.chapter_groups[].title`
- `data.title`
- `data.lock_message`
- `reward_tables/xxx.title`
- `chapters/xxx.title`
- `chapters/xxx.subtitle[]`
- `chapters/xxx.quests[].title`
- `chapters/xxx.quests[].subtitle`
- `chapters/xxx.quests[].tasks[].title`
- `chapters/xxx.quests[].rewards[].title`
- `chapters/xxx.quests[].description[]`

## Feature

### Continuous Translation Works 

After `.snbt` files were replaced by localization keys, you can still alter quest descriptions, titles etc. in FTBQuests GUI.

As long as you provide `.json` lang files that before your changes, `FTBQuestProfiler` will correctly recongnize your `.snbt` files (which are mixed in raw texts and localization keys), retain values presented in old lang files, and generate new localization keys according their sequential order! (OCD-friendly!)

### Localization Key Merge

When there are multiple lines of plain text strings in quest descriptions, `FTBQuestProfiler` can merge these strings into one large string, reducing the number of translation keys and making it easier for translators to work. This feature is enabled by default, but you can disable it in `config.ini` to keep each line of text corresponding to a separate translation key.

## Example

Note: Quest files in following examples are come from Minecraft modpack [Create: The Brass Concerto](https://github.com/Slimeli-32767/CreateTheBrassConcerto>)

### First Try

original `.snbt` file:
```s
{
	...
	filename: "158AAB195C2FD998"
	...
	id: "158AAB195C2FD998"
	...
	quests: [
		{
			...
			description: [
				"利用火箭发射台，你可以通过运载火箭建立自动化的星际物流网络！除此以外，你也可以随着运载火箭快捷地前往各个星球"
				""
				"[ \"如果你需要运送流体的话，你可以考虑使用\", { \"text\": \"密封储罐\", \"underlined\": \"true\", \"clickEvent\": { \"action\": \"change_page\", \"value\": \"37B807F2628934C1\" } }, \"！\" ]"
				""
				"&a在轨道发射运载火箭时，消耗的材料会更少！&r"
				""
				"&e需要注意的是，火箭自身不带有强加载！&r"
				""
				"&a在思索中查看具体结构或使用蓝图打印！请注意：蓝图不包含控制器，并且标注了方向的蓝图不能旋转！&r"
				""
				"&o温馨提示：如果莫名其妙停止工作，可以检查是否是区块掉加载导致的问题！&r"
				""
				"&e火箭的发射配方时间为320tick&r"
			]
			id: "70663CE0980E8D83"
			...
		}
	]
	title: "星空物流网络"
}
```

Transformed `.snbt` file:
```s
{
	...
	filename: "158AAB195C2FD998"
	...
	id: "158AAB195C2FD998"
	...
	quests: [{
		...
		description: [
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_01}"
			""
			"[\"\", {\"translate\": \"ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02.rich_01\"}, {\"underlined\": \"true\", \"clickEvent\": {\"action\": \"change_page\", \"value\": \"37B807F2628934C1\"}, \"translate\": \"ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02.rich_02\"}, {\"translate\": \"ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02.rich_03\"}]"
			""
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03}"
			""
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_04}"
			""
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_05}"
			""
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_06}"
			""
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_07}"
		]
		id: "70663CE0980E8D83"
		...
	}]
	title: "{ftbquests.chapter_158AAB195C2FD998.title}"
}
```

Generated `zh_cn.json`：
```json
{
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_01": "利用火箭发射台，你可以通过运载火箭建立自动化的星际物流网络！除此以外，你也可以随着运载火箭快捷地前往各个星球",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02.rich_01": "如果你需要运送流体的话，你可以考虑使用",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02.rich_02": "密封储罐",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02.rich_03": "！",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03": "&a在轨道发射运载火箭时，消耗的材料会更少！&r",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_04": "&e需要注意的是，火箭自身不带有强加载！&r",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_05": "&a在思索中查看具体结构或使用蓝图打印！请注意：蓝图不包含控制器，并且标注了方向的蓝图不能旋转！&r",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_06": "&o温馨提示：如果莫名其妙停止工作，可以检查是否是区块掉加载导致的问题！&r",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_07": "&e火箭的发射配方时间为320tick&r",
  "ftbquests.chapter_158AAB195C2FD998.title": "星空物流网络",
}
```

### Continuous Translation

Assuming your `.snbt` file were changed to this after some updated works:
```s
{
	...
	filename: "158AAB195C2FD998"
	...
	id: "158AAB195C2FD998"
	...
	quests: [{
		...
		description: [
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_01}"
			"我觉得这里需要补充一些文本，所以我补充了1111122222333333"
			""
			"[\"\", \"我觉得这里需要补充更多一些文本，所以我补充了\", {\"translate\": \"ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02.rich_01\"}, {\"underlined\": \"true\", \"clickEvent\": {\"action\": \"change_page\", \"value\": \"37B807F2628934C1\"}, \"text\": \"改动改动改动\"}, {\"translate\": \"ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02.rich_03\"}]"
			""
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03}"
			""
			"这里原来写的东西过时了，所以我改动了"
			""
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_05}"
			""
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_06}"
			""
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_07}"
		]
		id: "70663CE0980E8D83"
		...
	}]
	title: "{ftbquests.chapter_158AAB195C2FD998.title}"
}
```

At this time, you need to provide the original `.json` lang files as inputs:

`zh_cn.json`：
```json
{
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_01": "利用火箭发射台，你可以通过运载火箭建立自动化的星际物流网络！除此以外，你也可以随着运载火箭快捷地前往各个星球",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02.rich_01": "如果你需要运送流体的话，你可以考虑使用",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02.rich_02": "密封储罐",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02.rich_03": "！",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03": "&a在轨道发射运载火箭时，消耗的材料会更少！&r",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_04": "&e需要注意的是，火箭自身不带有强加载！&r",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_05": "&a在思索中查看具体结构或使用蓝图打印！请注意：蓝图不包含控制器，并且标注了方向的蓝图不能旋转！&r",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_06": "&o温馨提示：如果莫名其妙停止工作，可以检查是否是区块掉加载导致的问题！&r",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_07": "&e火箭的发射配方时间为320tick&r",
  "ftbquests.chapter_158AAB195C2FD998.title": "星空物流网络"
}
```

`en_us.json`：
```json
{
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_01": "Origin English text for description line 1",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02.rich_01": "Origin English text for rich text part 1",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02.rich_02": "Origin English text for rich text part 2",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02.rich_03": "！",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03": "Origin English text for description line 3",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_04": "Origin English text for description line 4",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_05": "Origin English text for description line 5",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_06": "Origin English text for description line 6",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_07": "Origin English text for description line 7",
  "ftbquests.chapter_158AAB195C2FD998.title": "Origin English text for chapter title"
}
```

After execute `FTBQuestProfiler`, you will get new `.snbt` files, new translation keys were generated:

```s
{
	...
	filename: "158AAB195C2FD998"
	...
	id: "158AAB195C2FD998"
	...
	quests: [{
		...
		description: [
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_01}"
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02}"
			""
			"[\"\", {\"translate\": \"ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03.rich_01\"}, {\"translate\": \"ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03.rich_02\"}, {\"underlined\": \"true\", \"clickEvent\": {\"action\": \"change_page\", \"value\": \"37B807F2628934C1\"}, \"translate\": \"ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03.rich_03\"}, {\"translate\": \"ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03.rich_04\"}]"
			""
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_04}"
			""
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_05}"
			""
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_06}"
			""
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_07}"
			""
			"{ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_08}"
		]
		id: "70663CE0980E8D83"
		...
	}]
	title: "{ftbquests.chapter_158AAB195C2FD998.title}"
}
```

The texts you altered will be added to all your `.json` lang files, but the original value will be retained for other unchanged texts.

`zh_cn.json`：
```json
{
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_01": "利用火箭发射台，你可以通过运载火箭建立自动化的星际物流网络！除此以外，你也可以随着运载火箭快捷地前往各个星球",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02": "我觉得这里需要补充一些文本，所以我补充了111112222233333",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03.rich_01": "我觉得这里需要补充更多一些文本，所以我补充了",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03.rich_02": "如果你需要运送流体的话，你可以考虑使用",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03.rich_03": "改动改动改动",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03.rich_04": "！",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_04": "&a在轨道发射运载火箭时，消耗的材料会更少！&r",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_05": "这里原来写的东西过时了，所以我改动了",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_06": "&a在思索中查看具体结构或使用蓝图打印！请注意：蓝图不包含控制器，并且标注了方向的蓝图不能旋转！&r",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_07": "&o温馨提示：如果莫名其妙停止工作，可以检查是否是区块掉加载导致的问题！&r",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_08": "&e火箭的发射配方时间为320tick&r",
  "ftbquests.chapter_158AAB195C2FD998.title": "星空物流网络"
}
```

`en_us.json`：

```json
{
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_01": "Origin English text for description line 1",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02": "我觉得这里需要补充一些文本，所以我补充了111112222233333",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03.rich_01": "我觉得这里需要补充更多一些文本，所以我补充了",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03.rich_02": "Origin English text for rich text part 1",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03.rich_03": "改动改动改动",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_03.rich_04": "！",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_04": "Origin English text for description line 3",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_05": "这里原来写的东西过时了，所以我改动了",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_06": "Origin English text for description line 5",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_07": "Origin English text for description line 6",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_08": "Origin English text for description line 7",
  "ftbquests.chapter_158AAB195C2FD998.title": "Origin English text for chapter title"
}
```