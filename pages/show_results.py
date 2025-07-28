from pages import *


st.set_page_config(
	layout="wide"
)

if not exist_path("contest"):
	warninng_load_file()

else:
	columns = st.columns([1, 3])

	with columns[0]:
		pass
			
	with columns[1]:
		pass