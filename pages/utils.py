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


def contest_year():
	return st.selectbox(
		'Год проведения соревнований',
		[n for n in range(1992, datetime.datetime.now().year + 1)],
		index=None,
		placeholder="Select contest year...",
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
			return fr"contest\{kwargs["contest"]}\{kwargs["other_params"][0]}m\{kwargs["year"]}\{kwargs["city"]} {kwargs["other_params"][1]} stage\{kwargs["title"]}"

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
	

def show_file(_bytes):
	if _bytes:
		base64_pdf = base64.b64encode(_bytes).decode("utf-8")

		# Встраиваем PDF через HTML
		pdf_display = f"""
		<iframe src="data:application/pdf; base64,{base64_pdf}" 
			width="100%" 
			height="800px" 
			style="border: none;">
		</iframe>
		"""
		st.markdown(pdf_display, unsafe_allow_html=True)