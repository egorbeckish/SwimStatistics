from pages import *


if "uploader_key" not in st.session_state:
	st.session_state.uploader_key = 0


contest = type_contest()
other_params = other_contest_params(contest)
year = contest_year()
city = contest_city()
files = load_files()


if files:
	for file in files:
		file_bytes = file.getvalue()
		title = get_title(file_bytes)
		path = save_path(contest=contest, other_params=other_params, year=year, city=city, title=title)
		save_file(file_bytes, path)
	
	
	st.session_state.uploader_key += 1
	st.rerun()
