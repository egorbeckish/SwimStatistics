from lib import (
	iso3166,
	datetime,
	requests,
	BeautifulSoup,
	re,
	regex,
	pprint,
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
		"start": start,
		"finish": finish,
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


def get_metadata(html: BeautifulSoup, pool):
	contest = get_contest(html)
	period_contest = get_period_contest(html)
	place = get_place(html)

	return contest | {"pool": pool} | period_contest | place


def get_days(html: BeautifulSoup):
	return html.find_all("div", class_="block-table")


def get_events(block: BeautifulSoup):
	return [row for row in block.find_all("div", class_="row") if row.find("p", class_="round").text]


def save_pdf(html: BeautifulSoup):
	block_days = get_days(html)

	for block_day in block_days:
		for a in block_day.find_all("div", class_="row")[1:]:
			print(a)
			...
		
	

def save_omega_results(url, pool):
	html = get_html(url)
	metadata = get_metadata(html, pool)
	save_pdf(html)
