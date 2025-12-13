from config import CONTEST_PATH
from lib import (
	os,
	json,
)


def create_dirs(path):
	os.makedirs(f"{CONTEST_PATH}/{path}", exist_ok=True)


def write_pdf(path, title, content):
	with open(f"{CONTEST_PATH}/{path}/pdf/{title}.pdf", "wb") as file:
		file.write(content)


def get_path(metadata):
	if "stage" in metadata:
		return f"{metadata["contest"]}/{metadata["pool"]}/{metadata["year"]}/{metadata["stage"]} stage"
	
	return f"{metadata["contest"]}/{metadata["pool"]}/{metadata["year"]}"


def save_metadata(path, metadata):
	with open(f"{CONTEST_PATH}/{path}/metadata.json", "w", encoding="utf-8") as file:
		json.dump(metadata, file, indent=4)


def create_regex_json(path):
	with open(f"{CONTEST_PATH}/{path}/parse.json", "w", encoding="utf-8") as file:
		json.dump(
			{
				"50": "",
				"100": "",
				"200": "",
				"400": "",
				"800": "",
				"1500": ""
			}, 
			file, 
			indent=4
		)
