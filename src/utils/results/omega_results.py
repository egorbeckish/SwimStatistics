from config import CONTEST_PATH
from lib import (
	iso3166,
	datetime,
	requests,
	BeautifulSoup,
	re,
	regex,
	pprint,
	os,
	json
)


def get_page(url):
	return requests.get(url).text


def get_html(url):
	page = get_page(url)
	return BeautifulSoup(page, "html.parser")


def get_place(html: BeautifulSoup):
	subtitle = html.find("p", class_="subtitle").text
	place = re.search(
		r"(?P<city>[a-zA-Z]+)\,\s(?P<alpha3>[a-zA-Z]{3,})",
		subtitle
	).groupdict()

	place["country"] = iso3166.countries[place["alpha3"]].name
	return place


def str_to_datetime(date_string):
	# date_datetime = datetime.datetime.strptime(date_string, "%d %B %Y").date()
	# return date_datetime

	return datetime.datetime.strptime(date_string, "%d %B %Y").date()


def get_period_contest(html: BeautifulSoup):
	start, *_, finish = map(lambda x: x.text.split(", ")[-1][:-1] , html.find_all("div", class_="row date"))
	start, finish = str_to_datetime(start), str_to_datetime(finish)
	
	return {
		"start": start.isoformat(),
		"finish": finish.isoformat(),
		"year": finish.year
	}


def type_contest(contest):
	contest_regex = regex.search(
		r"(?P<type>World|European)\sAquatics\s(?:(?:(?P<junior>Junior)|(?P<pool>Short\sCourse))\s)?(?:(?:Swimming)\s)?(?P<contest>Championships|World\sCup)",
		contest
	)
	
	if contest_regex:
		contest = contest_regex.groupdict()
		
		if contest["type"] in contest["contest"]:
			return contest["contest"]
		
		if contest["junior"]:
			return f"{contest["type"]} {contest["junior"]} {contest["contest"]}"
			
		return f"{contest["type"]} {contest["contest"]}"

	return contest


def get_contest(html: BeautifulSoup):
	contest = type_contest(html.find("h1").text)
	
	return {"contest": contest}


def get_metadata(html: BeautifulSoup, pool, stage=None):
	contest = get_contest(html)
	period_contest = get_period_contest(html)
	place = get_place(html)

	if stage:
		return contest | {"stage": stage} | {"pool": pool} | period_contest | place
	
	return contest | {"pool": pool} | period_contest | place


def get_days(html: BeautifulSoup):
	return html.find_all("div", class_="block-table")


def get_events(block: BeautifulSoup):
	return [row for row in block.find_all("div", class_="row")[1:] if row.find("p", class_="round").text]


def get_event_regex(event):
	event_regex = re.search(
		r"(?P<sex>[a-zA-Z]+\'s)\s(?P<style>Freestyle|Backstroke|Butterfly|Breaststroke|Medley)\s(?P<distance>[\d]{2,4}m)\s+((Slowest|Fastest)\s)?(?P<stage>Heats|Semi-finals|Final|Semifinals|Heat)\s?(?P<swim_off>(?:Swim-off|Swim-Off))?", 
		event
	)

	event_regex = event_regex.groupdict() if event_regex else None
	return None if (not event_regex or event_regex["swim_off"]) else event_regex


def get_event(row: BeautifulSoup):
	event = get_event_regex(row.find("p", class_="round").text)

	if event:
		event["style"] = "IM" if event["style"] == "Medley" else event["style"].lower()
		return f"{event["distance"]} {event["style"]} {event["sex"]} {event["stage"]}"

	return event


def get_link(row: BeautifulSoup):
	return f"https://www.omegatiming.com{row.find_all("a")[-1]["href"]}"


def get_content(link):
	return requests.get(link).content


def create_dirs(path):
	os.makedirs(f"{CONTEST_PATH}/{path}", exist_ok=True)


def write_pdf(path, title, content):
	with open(f"{CONTEST_PATH}/{path}/{title}.pdf", "wb") as file:
		file.write(content)


def get_path(metadata):
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


def save_files(html: BeautifulSoup, metadata):
	block_days = get_days(html)
	path = get_path(metadata)
	
	create_dirs(path)
	save_metadata(path, metadata)
	create_regex_json(path)
	
	for block_day in block_days:
		events = get_events(block_day)

		for row in events:
			if event := get_event(row):
				link = get_link(row)
				pdf = get_content(link)
				write_pdf(path, event, pdf)


def omega_save_results(url, pool, stage=None):
	html = get_html(url)
	metadata = get_metadata(html, pool, stage)
	pprint(metadata, sort_dicts=False)
	# save_files(html, metadata)
