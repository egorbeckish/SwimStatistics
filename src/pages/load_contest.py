from lib import (
	st,
	datetime,
	uuid,
	pprint
)


from utils import (
	validate_input,
	exist_city,
	omega_save_results,
	standart_save_results
)


st.set_page_config(
	layout="wide"
)


columns = st.columns([.9, .1], gap="large")


with columns[0]:
	st.title("Load Contest")
	stage = None
	pool = None

	standart_load, omega_load = st.tabs(["Standart", "Omega"])

	with standart_load:
		contest = st.selectbox(
			"Contest",
			["World Cup", "World Championship"],
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
				key=st.session_state["widget_standart_pool"],
				help="m - meters, y - yard",
				placeholder="Choose pool...",
				disabled=False if contest else True
			)

		place = st.text_input(
			"Place",
			key="widget_place",
			on_change=exist_city,
			args=(
				"widget_place",
			),
			placeholder="Write place/city contest...",
			disabled=False if contest else True
		)

		date = st.date_input(
			"Date",
			(datetime.datetime(1896, 4, 6), datetime.datetime.now()),
			key=st.session_state["widget_date"],
			format="DD.MM.YYYY",
			disabled=False if contest else True
		)

		# load_files = st.file_uploader(
		# 	"Load files",
		# 	accept_multiple_files=True,
		# 	key=st.session_state["widget_file_uploader"],
		# 	disabled=not all([contest, stage if contest == "World Cup" else True, pool, not st.session_state["widget_access_input"], date])
		# )

		load_files = all([contest, stage if contest == "World Cup" else True, pool, not st.session_state["widget_access_input"], date])

		if st.button(
			"Load",
			disabled=False if load_files else True
		):
			with st.spinner(show_time=True):
				standart_save_results(
					contest=contest,
					stage=stage,
					pool=pool,
					place=place,
					date=date
				)
			
			st.session_state["widget_contest"] = uuid.uuid4()
			st.session_state["widget_stage"] = uuid.uuid4()
			st.session_state["widget_standart_pool"] = uuid.uuid4()
			st.session_state["widget_date"] = uuid.uuid4()
			st.session_state["widget_file_uploader"] = uuid.uuid4()
			st.session_state["widget_access_input"] = True

			del st.session_state["widget_place"]
			st.session_state.widget_place = ""
			
			st.rerun()
	
	with omega_load:
		tmp_link = st.code("https://www.omegatiming.com/2025/world-aquatics-swimming-world-cup03-live-results")
	
		omega_link = st.text_input(
			"Omega Link",
			key="widget_omega_link",
			on_change=validate_input,
			args=(
				"widget_omega_link",
				r"https:\/\/www.omegatiming\.com\/[\d]{4}\/[A-Za-z0-9\-]+",
			),
			placeholder="Write link..."
		)

		if "cup" in omega_link:
			stage = st.selectbox(
				"Stage Cup",
				["I", "II", "III"],
				None,
				key=st.session_state["widget_stage"],
				placeholder="Choose stage...",
			)

		pool = st.selectbox(
			"Pool (meters)",
			["25m", "50m"],
			None,
			key=st.session_state["widget_omega_pool"],
			placeholder="Choose pool...",
			disabled=False if omega_link else True
		)
		
		if st.button(
			"Get",
			disabled=not all([not st.session_state["widget_access_input"], stage if "cup" in omega_link else True, pool])
		):
			
			with st.spinner(show_time=True):
				omega_save_results(omega_link, pool, stage)


			del st.session_state["widget_omega_link"]
			st.session_state.widget_omega_link = ""
			
			st.session_state["widget_access_input"] = True
			st.session_state["widget_stage"] = uuid.uuid4()
			st.session_state["widget_pool"] = uuid.uuid4()
			st.session_state["widget_omega_pool"] = uuid.uuid4()
			
			st.rerun()


with columns[1]:
	st.write("Pages")
	st.page_link("main.py")
	st.page_link("pages/exit.py")
