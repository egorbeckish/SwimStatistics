from statistic import *


def get_style(style):
	return "IM" if style in ["IM", "Individual Medley"] else style.lower()


def get_stage(stage):
	if not stage:
		return "Final"
	
	[stage] = stage.capturesdict()["stage"]
	if stage in ["Preliminaries"]:
		stage = "Heats"
	
	return stage


def get_sex(sex):
	if "'s" not in sex:
		return sex + "'s"
	
	return sex


def get_data(**kwargs):
	for k, v in kwargs.items():
		[kwargs[k]] = v
	
	kwargs["style"] = get_style(kwargs["style"])
	kwargs["sex"] = get_sex(kwargs["sex"])
	kwargs["unit"] = kwargs["unit"].lower()
	return kwargs


def join_title(**kwargs):
	match kwargs["unit"]:
		case "m":
			return f"{kwargs["distance"]}{kwargs["unit"]} {kwargs["style"]} {kwargs["sex"]} {kwargs["stage"]}.pdf"

		case "yard":
			return f"{kwargs["distance"]} {kwargs["unit"]} {kwargs["style"]} {kwargs["sex"]} {kwargs["stage"]}.pdf"
		

def get_title(file_bytes):
	with pdfplumber.open(BytesIO(file_bytes)) as data:
		data = data.pages[0].extract_text()
	
	regex_data = regex.finditer(EVENT, data).search().capturesdict()
	title = get_data(**regex_data)

	stage = regex.finditer(STAGE, data).search()
	stage = get_stage(stage)

	title["stage"] = stage
	return join_title(**title)


def get_regex_data(text, **kwargs):
	if kwargs["contest"] in ["World Championship", "World Cup"]:
		pass

	elif kwargs["contest"] in ["Olympic Games", "University"]:
		pattern = REGEX_DISTANCE[kwargs["unit"]]["50"][kwargs["distance"]][kwargs["stage"]]
		data = [data for data in regex.finditer(pattern, text)]

	elif kwargs["contest"] == "NCAA":
		pass

	if kwargs["unload"]:
		for i in range(len(data)):
			data[i] = data[i].capturesdict()
	
	st.code(pattern, language=None)
	return data