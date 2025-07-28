from pages import *


def type_contest():
	return st.selectbox(
		"Выберите тип соревнований",
		TYPE_CONTEST,
		index=None,
		placeholder="Select contest...",
	)


def other_contest_params(type_contest):
	match type_contest:
		case "World Cup":
			pool = st.selectbox(
				"Выберите длину бассейна",
				POOL_DISTANCE,
				index=None,
				placeholder="Select pool distance..."
			)

			stage = st.selectbox(
				"Выберите этап кубка мира",
				WORLD_CUP_STAGE,
				index=None,
				placeholder="Select stage..."
			)
			return pool, stage
		
		case "NCAA":
			return st.selectbox(
				"Выберите пол",
				SEX,
				index=None,
				placeholder="Select sex..."
			)
		
		case "World Championship":
			return st.selectbox(
				"Выберите длину бассейна",
				POOL_DISTANCE,
				index=None,
				placeholder="Select pool distance..."
			)


def contest_date():
	return st.date_input(
		'Дата проведения соревнований',
		(datetime.datetime.now().date(), datetime.datetime.now().date()),
		format="DD.MM.YYYY",
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
	kwargs["date"] = f"{kwargs["date"][0].strftime("%d.%m.%Y")}-{kwargs["date"][1].strftime("%d.%m.%Y")}"

	match kwargs["contest"]:
		case "World Championship":
			pass

		case "World Cup":
			pass

		case _:
			return fr"contest\{kwargs["contest"]}\{kwargs["city"]}\{kwargs["other_params"]}\{kwargs["date"]}\{kwargs["title"]}"

	return kwargs


def make_dir(path):
	path = r"\\".join(path.split("\\")[:-1])
	os.makedirs(path, exist_ok=True)


def save_file(file_bytes, save_path):
	make_dir(save_path)
	with open(save_path, "wb") as file:
		file.write(file_bytes)