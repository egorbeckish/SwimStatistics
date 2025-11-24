from lib import (
	re, 
	st
)


def validate_link(pattern):
	link_input = st.session_state["link_input"]

	if re.search(pattern, link_input):
		st.session_state["access_link"] = False
	