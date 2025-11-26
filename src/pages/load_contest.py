from lib import (
	st,
	datetime,
	uuid,
	pprint
)


from utils import (
	validate_link, 
	save_omega_results
)


from config import load_env


st.set_page_config(
	layout="wide"
)


columns = st.columns([.9, .1], gap="large")
load_env()
pprint(dict(st.session_state))

with columns[0]:
	st.title("Load Contest")
	stage = None
	pool = None

	standart_load, omega_load = st.tabs(["Standart", "Omega"])

	with standart_load:
		contest = st.selectbox(
			"Contest",
			["World Cup"],
			None,
			key=st.session_state["widget_contest"],
			placeholder="Choose contest...",
		)

		if contest == "World Cup":
			stage = st.selectbox(
				"Stage Cup",
				["I", "II", "III"],
				None,
				key=st.session_state["widget_stage"],
				placeholder="Choose stage...",
			)

		if contest not in [None, "Olympic Games", "Univercity", "NCAA"]:
			pool = st.selectbox(
				"Pool",
				["25m", "50m", "25y", "50y"],
				None,
				key=st.session_state["widget_pool"],
				help="m - meters, y - yard",
				placeholder="Choose pool...",
				disabled=False if contest else True
			)

		place = st.text_input(
			"Place",
			key=st.session_state["widget_place"],
			placeholder="Write place contest... For example: Hungary HUN",
			disabled=False if contest else True
		)

		date = st.date_input(
			"Date",
			(datetime.datetime(1896, 4, 6), datetime.datetime.now()),
			key=st.session_state["widget_date"],
			format="DD.MM.YYYY",
			disabled=False if contest else True
		)

		load_files = st.file_uploader(
			"Load files",
			accept_multiple_files=True,
			key=st.session_state["widget_file_uploader"],
			disabled=not all([contest, stage, pool, place, date])
		)

		if st.button(
			"Load",
			disabled=False if load_files else True
		):
			with st.spinner(show_time=True):
				pass
			
			st.session_state["widget_contest"] = uuid.uuid4()
			st.session_state["widget_stage"] = uuid.uuid4()
			st.session_state["widget_pool"] = uuid.uuid4()
			st.session_state["widget_place"] = uuid.uuid4()
			st.session_state["widget_date"] = uuid.uuid4()
			st.session_state["widget_file_uploader"] = uuid.uuid4()
			st.rerun()
	
	with omega_load:
		tmp_link = st.code("https://www.omegatiming.com/2025/world-aquatics-swimming-world-cup03-live-results")
	
		omega_link = st.text_input(
			"Omega Link",
			key="widget_link_input",
			on_change=validate_link,
			args=(
				r"https:\/\/www.omegatiming\.com\/[\d]{4}\/[A-Za-z0-9\-]+",
			)
		)

		if st.button(
			"Get",
			disabled=st.session_state["widget_access_link"]
		):
			
			with st.spinner(show_time=True):
				save_omega_results(omega_link)


			del st.session_state["widget_link_input"]
			del st.session_state["widget_access_link"]
			st.session_state.link_input = ""
			st.session_state.access_link = True
			st.rerun()


with columns[1]:
	st.write("Pages")
	st.page_link("main.py")
	st.page_link("pages/exit.py")
