from lib import (
	iso3166,
	datetime,
	requests,
	BeautifulSoup,
	re,
	pprint,
)


def get_page(url):
	return requests.get(url).text


def convert_str_to_html(content):
	return BeautifulSoup(content, "html.parser")


def month_str_to_int(month):
	pass


def get_place(html: BeautifulSoup):
	subtitle = html.find("p", class_="subtitle").text
	place = re.search(
		r"(?P<city>[a-zA-Z]+)\,\s(?P<alpha3>[a-zA-Z]{3,})",
		subtitle
	).groupdict()

	place["country"] = iso3166.countries[place["alpha3"]].name
	return place


def str_to_datetime(date_string):
	date_datetime = datetime.datetime.strptime(date_string, "%d %B %Y").date()
	return date_datetime


def get_period_contest(html: BeautifulSoup):
	start, *_, finish = map(lambda x: x.text.split(", ")[-1][:-1] , html.find_all("div", class_="row date"))
	start, finish = str_to_datetime(start), str_to_datetime(finish)
	return {
		"start": start,
		"finish": finish,
		"year": finish.year
	}


def type_contest(contest):
	contest_regex = re.search(
		r"(?P<type>World|European)\sAquatics\s(?:(?:(?P<junior>Junior)|(?:Short\sCourse))\s)?(?:(?:Swimming)\s)?(?P<contest>Championships|World\sCup)",
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


def get_metadata(html: BeautifulSoup):
	contest = get_contest(html)
	period_contest = get_period_contest(html)
	place = get_place(html)

	return contest | period_contest | place


def save_omega_results(url):
	page = get_page(url)
	html = convert_str_to_html(page)
	metadata = get_metadata(html)
	pprint(metadata, sort_dicts=False)