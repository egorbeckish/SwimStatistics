from lib import (
	os,
	load_dotenv,
	dotenv_values,
	st,
	literal_eval
)


CONTEST_PATH = f"{os.path.dirname(os.getcwd())}/contest"


def load_env():
	if st.session_state:
		return
	
	env_path = f"{os.path.dirname(__file__)}/.env"
	envirements = dict()
	for file_env in os.listdir(env_path):
		if file_env.startswith(".env."):
			# load_dotenv(os.path.join(env_path, file_env))
			envirements.update(dotenv_values(os.path.join(env_path, file_env)))


	for k, v in envirements.items():
		st.session_state[k.lower()] = v if v == "" else literal_eval(v)

	st.toast("Данные получены", icon="✅")
