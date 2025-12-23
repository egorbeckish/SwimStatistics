from lib import (
	pprint,
	iso3166,
	GeonamesCache,
	pdfplumber,
	BytesIO,
	re
)


from .utils import (
	get_path,
	save_metadata,
	create_dirs,
	create_regex_json,
	write_pdf
)


def get_stage(metadata):
	if metadata["stage"] is None:
		del metadata["stage"]


def get_period_contest(metadata: dict):
	start, finish = metadata["date"]
	
	metadata.update(
		{
			"start": start.isoformat(),
			"finish": finish.isoformat(),
			"year": start.year
		}
	)

	del metadata["date"]
	

def get_place(metadata: dict):
	alpha2 = list(GeonamesCache().get_cities_by_name(metadata["place"])[0].values())[0]["countrycode"]
	country_data = iso3166.countries_by_alpha2[alpha2]
	
	metadata.update(
		{
			"city": metadata["place"],
			"alpha3": country_data.alpha3,
			"country": country_data.name,
		}
	)

	del metadata["place"]


def get_metadata(**kwargs):
	get_stage(kwargs)
	get_period_contest(kwargs)
	get_place(kwargs)

	
	return kwargs


def get_event_regex(page):
	return re.search(
		r"(?P<sex>Men's|Women's)\s(?P<distance>[\d]{2,4}m)\s(?P<style>Freestyle|Backstroke|Breaststroke|Butterfly|Individual\sMedley)",
		page
	).groupdict() | re.search(r"(?P<stage>Final|Semifinals|Heats|Slowest\sHeats)", page).groupdict()


def get_event(page):
	event = get_event_regex(page)

	event["style"] = "IM" if event["style"] == "Individual Medley" else event["style"].lower()

	if event["stage"] == "Slowest Heats":
		event["stage"] = "Heats"
	
	elif event["stage"] is None:
		event["stage"] = "Final"

	return f"{event["distance"]} {event["style"]} {event["sex"]} {event["stage"]}"


def get_title_page(file):
	with pdfplumber.open(BytesIO(file.getvalue())) as pdf:
		return pdf.pages[0].extract_text()


def save_files(metadata):
	path = get_path(metadata)
	files = metadata["load_files"]
	del metadata["load_files"]

	create_dirs(f"{path}/pdf")
	save_metadata(path, metadata)
	create_regex_json(path)

	for file in files:
		title_page = get_title_page(file)
		event = get_event(title_page)
		write_pdf(path, event, file.getvalue())


def standart_save_results(**kwargs):
	metadata = get_metadata(**kwargs)
	save_files(metadata)
