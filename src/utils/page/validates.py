from lib import (
	re, 
	st
)


def validate_input(widget, pattern):
	if re.search(pattern, st.session_state[widget]):
		st.session_state["widget_access_input"] = False
	
	else:
		st.session_state["widget_access_input"] = True