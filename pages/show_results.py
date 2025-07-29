from pages import *


st.set_page_config(
	layout="wide"
)

if not exist_path("contest"):
	warninng_load_file()

else:
	columns = st.columns([1, 3])

	with columns[0]:
		contest = show_contest()
		info = show_info(contest)
			
	with columns[1]:
		if info:
			if all([item != None for item in info]):
				show_file(*info)