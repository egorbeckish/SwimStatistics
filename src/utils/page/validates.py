from lib import (
	re, 
	st,
	GeonamesCache
)


def validate_input(widget, pattern):
	if re.search(pattern, st.session_state[widget]):
		st.session_state["widget_access_input"] = True
	
	else:
		st.session_state["widget_access_input"] = False


def exist_city(widget):
	if GeonamesCache().get_cities_by_name(st.session_state[widget]):
		st.session_state["widget_access_input"] = True
	
	else:
		st.session_state["widget_access_input"] = False


def correct_date(widget):
	if len(st.session_state[widget]) == 2:
		start, finish = st.session_state[widget]
		
		if 2 <= (finish - start).days + 1 <= 10:
			st.session_state["widget_access_date"] = True

		else:
			st.session_state["widget_access_date"] = False

	else:
		st.session_state["widget_access_date"] = False
