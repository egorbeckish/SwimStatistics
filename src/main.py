from lib import st
from config import load_env


st.set_page_config(
	layout="wide"
)

load_env()
# pprint(dict(st.session_state))

columns = st.columns([.9, .1], gap="large")


with columns[0]:
	st.title("Main Page")


with columns[1]:
	st.write("Pages")
	st.page_link("pages/load_contest.py")
	st.page_link("pages/exit.py")
