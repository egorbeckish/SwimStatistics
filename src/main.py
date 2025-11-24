from lib import st


st.set_page_config(
	layout="wide"
)

columns = st.columns([.9, .1], gap="large")


with columns[0]:
	st.title("Main Page")


with columns[1]:
	st.write("Pages")
	st.page_link("pages/load_contest.py")
	st.page_link("pages/exit.py")
