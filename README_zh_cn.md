# FTBQuestProfiler

其他语言:
- [[美式英语 / American English / en_us]](README.md)

## 使用

1. clone 该仓库至本地，切换至 `main` 分支
2. 配置好 Python 环境（推荐 3.12+），按照 `requirements.txt` 安装所需包
3. 修改 `config.ini` 中的配置项
4. 在项目目录运行 `python ./main.py`
5. （走你）

## `config.ini` 配置项解释

- `ftbquests.lang` 你在编写任务时所使用的语言，默认为 `zh_cn`
- `ftbquests.input_directory` 用于输入的 FTBQuests 目录，目录结构应完全符合 FTBQuests 生成的目录格式；通常为 `{modpack_dir}/config/ftbquests/quests`
- `ftbquests.output_directory` 用于输出的 FTBQuests 目录；若将值设为与 `ftbquests.input_directory` 相同，将**直接覆盖**原有的文件
- `lang.input_directory` 用于输入的语言文件目录，若无可留空，通常为 `{modpack_dir}/kubejs/assets/{somename}/lang`
- `lang.output_directory` 用于输出的语言文件目录；若将值设为与 `lang.input_directory` 相同，将**直接覆盖**原有的文件
- `lang.out_namespace` 生成的语言文件中翻译键的公共前缀，默认为 `ftbquests`
- `lang.sort` 是否对生成的语言文件进行键排序，默认为 `True`
- `general.logging` 是否在控制台打印日志，默认为 `True`

## 功能

`FTBQuestProfiler` 将 FTBQuests mod（<= Minecraft 1.20）生成的 `.snbt` 文件中的描述性文本替换为翻译键，并生成对应的 `.json` 语言文件以供翻译。支持富文本，`JSON` 对象（任务链接）。

### 支持的字段

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

## 特色

### 可持续的任务翻译工作

当 `.snbt` 文件被翻译键转化之后，你可以继续在 FTBQuests 的 GUI 中修改任务描述、标题等。只要你提供了修改前的 `.json` 语言文件，`FTBQuestProfiler` 将正确识别你输入的由原始字符串、翻译键所杂糅的 `.snbt` 文件，保留原有翻译键的值，并重新根据先后顺序生成对应的翻译键（强迫症福音）！

## 用例展示

注：以下展示的例子中出现的任务文件均来自于 Minecraft 整合包 [机械动力：黄铜协奏曲](https://github.com/Slimeli-32767/CreateTheBrassConcerto>)

### 第一次翻译

原始 `.snbt`：
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

转化后 `.snbt` 文件：
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

生成的 `zh_cn.json`：
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

### 可持续翻译

假设在某次任务更新工作完成之后，你的 `.snbt` 文件变为如下：
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
			"我觉得这里需要补充一些文本，所以我补充了"
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

此时，你只需要同时将原先的翻译 `.json` 文件作为输入：

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

运行 `FTBQuestProfiler` 后，得到新的 `.snbt` 文件，新的翻译键有着全新的编号：

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

修改过的文本会添加至所有 `.json` 文件之中，但原有的值会保持不变：

`zh_cn.json`：
```json
{
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_01": "利用火箭发射台，你可以通过运载火箭建立自动化的星际物流网络！除此以外，你也可以随着运载火箭快捷地前往各个星球",
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02": "我觉得这里需要补充一些文本，所以我补充了",
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
  "ftbquests.chapter_158AAB195C2FD998.quest_70663CE0980E8D83.desc_02": "我觉得这里需要补充一些文本，所以我补充了",
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