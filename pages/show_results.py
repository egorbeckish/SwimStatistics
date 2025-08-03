from pages import *


st.set_page_config(
	layout="wide"
)

if not exist_path("contest"):
	warninng_load_file()

else:
	columns = st.columns([1, 3])
	with columns[0]:
		
		_columns = st.columns([6, 1])
		with _columns[0]:
			contest = show_contest()

		with _columns[1]:
			for _ in range(2):
				st.write("")
			text = st.toggle("l", help="Показать текстом", label_visibility="hidden")
		
		info = show_info(contest)
			
	with columns[1]:
		if info:
			if all([item != None for item in info]):
				if text:
					st.code(show_text_file(*info), language=None)
					print(show_text_file(*info))
				
				else:
					show_file(*info)