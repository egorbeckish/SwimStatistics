from lib import (
	iso3166,
	datetime,
	requests,
	BeautifulSoup,
	re,
)


def get_page(url):
	return requests.get(url).text


def convert_str_to_html(content):
	return BeautifulSoup(content, "html.parser")


def month_str_to_int(month):
	pass


def get_period_contest(start, finish, month, month2, **kwargs):
	return start, finish, month, month2


def get_metadata(html: BeautifulSoup):
	place = html.find("p", class_="subtitle").text
	data = re.search(
		r"(?P<month>[a-zA-Z]+)\s(?P<date>(?P<start>[\d]{1,2})[a-zA-Z]{2}\sto\s(?P<month2>[a-zA-Z]+\s)?(?P<finish>[\d]{1,2})[a-zA-Z]{2})\s(?P<year>[\d]{4})\s\-\s(?P<city>[a-zA-Z]+)\,\s(?P<country>[a-zA-Z]{3,})",
		place
	).groupdict()

	period_contest = get_period_contest(**data)
	return period_contest


def save_omega_results(url):
	page = get_page(url)
	html = convert_str_to_html(page)
	metadata = get_metadata(html)
	print(metadata)