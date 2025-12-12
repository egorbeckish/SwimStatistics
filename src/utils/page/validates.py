from lib import (
	re, 
	st,
	GeonamesCache
)


def validate_input(widget, pattern):
	if re.search(pattern, st.session_state[widget]):
		st.session_state["widget_access_input"] = False
	
	else:
		st.session_state["widget_access_input"] = True


def exist_city(widget):
	if GeonamesCache().get_cities_by_name(st.session_state[widget]):
		st.session_state["widget_access_input"] = False
	
	else:
		st.session_state["widget_access_input"] = True
