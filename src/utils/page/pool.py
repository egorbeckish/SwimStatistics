from lib import st


def get_pool(contest):
	if contest == "NCAA":
		return "25y"
	
	elif contest in ["Olympic Game", "University"]:
		return "50m"
	
	return st.selectbox(
		"Pool",
		["25m", "50m", "25y", "50y"],
		None,
		key=st.session_state["widget_standart_pool"],
		help="m - meters, y - yard",
		placeholder="Choose pool...",
	)