from pages import *


def selectbox(title, options, placeholder=None):
	return st.selectbox(
		label=title,
		options=options,
		index=None,
		placeholder=placeholder
	)


def type_contest():
	return selectbox(
		"Выберите тип соревнований",
		TYPE_CONTEST,
		"Select contest..."
	)


def other_contest_params(type_contest):
	match type_contest:
		case "World Cup":
			pool = selectbox(
				"Выберите длину бассейна",
				POOL_DISTANCE,
				"Select pool..."
			)

			stage = selectbox(
				"Выберите этап кубка мира",
				WORLD_CUP_STAGE,
				"Select stage..."
			)
			
			return pool, stage
		
		case "NCAA":
			return selectbox(
				"Выберите пол",
				SEX,
				"Select sex..."
			)
		
		case "World Championship":
			return selectbox(
				"Выберите длину бассейна",
				POOL_DISTANCE,
				"Select pool..."
			)


def contest_year():
	return selectbox(
		'Год проведения соревнований',
		[n for n in range(1992, datetime.datetime.now().year + 1)][::-1],
		"Select year..."
	)


def contest_city():
	return st.text_input(
		'Название города и сокращение страны', 
		placeholder='Example: Budapest (HUN)',
		help='Возьмите из любого протокола, который вы загружаете'
	)


def load_files():
	return st.file_uploader(
		"Choose a PDF file",
		type=['pdf'],
		accept_multiple_files=True,
		help='Принимается только формат .pdf',
		key=st.session_state.uploader_key
	)


def save_path(**kwargs):
	match kwargs["contest"]:
		case "World Championship":
			return fr"contest\{kwargs["contest"]}\{kwargs["other_params"]}m\{kwargs["year"]}\{kwargs["city"]}\{kwargs["title"]}"

		case "World Cup":
			return fr"contest\{kwargs["contest"]}\{kwargs["other_params"][0]}m\{kwargs["year"]}\{kwargs["other_params"][1]} Stage I{kwargs["city"]}\{kwargs["title"]}"
		
		case "NCAA":
			return fr"contest\{kwargs["contest"]}\{kwargs["year"]}\{kwargs["city"]}\{kwargs["other_params"]}\{kwargs["title"]}"

		case _:
			return fr"contest\{kwargs["contest"]}\{kwargs["year"]}\{kwargs["city"]}\{kwargs["title"]}"

	return kwargs


def make_dir(path):
	path = r"\\".join(path.split("\\")[:-1])
	os.makedirs(path, exist_ok=True)


def save_file(file_bytes, save_path):
	make_dir(save_path)
	with open(save_path, "wb") as file:
		file.write(file_bytes)


def exist_path(path):
	return os.path.exists(path)


def warninng_load_file():
	st.warning(
		"Загрузите файлы",
		icon="⚠️"
	)


def get_data(*args):
	return os.listdir(fr"contest\{"\\".join(args)}")


def show_contest():
	return selectbox(
		"Выберите прошедшие соревнования",
		get_data(),
		"Select contest..."
	)


def show_info(contest):
	match contest:
		case "World Championship":
			pool = selectbox(
				"Выберите бассейн, в котором проходили соревнования",
				get_data(contest),
				"Select pool..."
			)

			year = selectbox(
				"Выберите год проведения соревнования",
				get_data(contest, pool) if pool else None,
				"Select year..."
			)

			[city] = get_data(contest, pool, year) if year else [None]

			files = selectbox(
				"Выберите результат",
				get_data(contest, pool, year, city) if year else None,
				"Select file..."
			)

			return contest, pool, year, city, files


		case "World Cup":
			pool = selectbox(
				"Выберите бассейн, в котором проходили соревнования",
				get_data(contest),
				"Select pool",
			)

			year = selectbox(
				"Выберите год проведения соревнования",
				get_data(contest, pool) if pool else None,
				"Select year",
			)

			stage = selectbox(
				"Выберите стадию",
				get_data(contest, pool, year) if year else None,
				"Select stage..."
			)

			files = selectbox(
				"Выберите результат",
				get_data(contest, pool, year, stage) if stage else None,
				"Select file..."
			)

			return contest, pool, year, stage, files
		
		case "NCAA":
			year = selectbox(
				"Выберите год проведения соревнования",
				get_data(contest),
				"Select year"
			)

			[city] = get_data(contest, year) if year else [None]

			sex = selectbox(
				"Выберите кто соревнуется",
				get_data(contest, year, city) if city else None,
				"Select sex..."
			)

			files = selectbox(
				"Выберите результат",
				get_data(contest, year, city, sex) if sex else None,
				"Select file..."
			)

			return contest, year, city, sex, files
	
	if contest in ["Olympic Games", "University"]:
		year = selectbox(
			"Выберите год проведения соревнования",
			get_data(contest),
			"Select year..."
		)

		[city] = get_data(contest, year) if year else [None]

		files = selectbox(
			"Выберите результат",
			get_data(contest, year, city) if city else None,
			"Select file..."
		)

		return contest, year, city, files


def get_file_bytes(*args):
	with open(fr"contest\{"\\".join(args)}", "rb") as file:
		_bytes = file.read()
	
	return _bytes

def show_file(*args):
	_bytes = get_file_bytes(*args)
	base64_pdf = base64.b64encode(_bytes).decode("utf-8")
	
	pdf_display = f"""
	<iframe src="data:application/pdf; base64,{base64_pdf}" 
		width="100%" 
		height="800px" 
		style="border: none;">
	</iframe>
	"""
	st.markdown(pdf_display, unsafe_allow_html=True)


def show_text_file(*args):
	with pdfplumber.open(fr"contest\{"\\".join(args)}" if len(args) > 1 else args[0]) as file:
		text = "\n".join([page.extract_text() for page in file.pages])

	# return regex.sub(r"\s\(\=?\d\)", "", text)
	return regex.sub(r"\s[\d]{2,4}m", "", regex.sub(r"\s\(\=?\d\)", "", text))


def get_distance_title(title):
	if title.split(maxsplit=2)[1] == "yard":
		pass

	return title[:title.index("m")]

def get_params_results(**kwargs):
	if kwargs["contest"] in ["World Cup", "World Championship"]:
		return REGEX_DISTANCE["m"][kwargs["pool"]][kwargs["distance"]]

	elif kwargs["contest"] in ["Olympic Games", "University"]:
		return REGEX_DISTANCE["m"]["50"][kwargs["distance"]]
	
	elif kwargs["contest"] == "NCAA":
		return REGEX_DISTANCE["yard"]


def get_results(**kwargs):
	pattern = get_params_results(**kwargs)
	text = show_text_file(kwargs["path"])
	
	results = []
	for data in regex.finditer(pattern, text):
		data = data.capturesdict()
		[place] = data["place"]
		[lane] = data["lane"]
		[surname] = data["surname"]
		[name] = data["name"]
		[country] = data["country"]
		[reaction_time] = data["reaction_time"]
		[finish_time] = data["finish_time"]
		result = place, lane, surname, name, country, reaction_time, finish_time
		results += [result]
	
	path = kwargs["path"].replace(kwargs["title"], fr"csv\{kwargs["title"][:-3]}csv")
	make_dir(path)
	write_csv_results(
		path,
		["Place", "Lane", "Surname", "Name", "Country", "RT", "FT"],
		results
	)
	

def write_csv_results(path, title, rows):
	with open(path, "w", newline="") as f:
		writer = csv.writer(f, delimiter="|")
		writer.writerow(title)
		writer.writerows(rows)