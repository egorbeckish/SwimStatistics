from lib import (
	pprint,
	iso3166,
	GeonamesCache
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
			"country": country_data.name,
			"city": metadata["place"],
			"alpha3": country_data.alpha3
		}
	)

	del metadata["place"]


def get_metadata(**kwargs):
	get_stage(kwargs)
	get_period_contest(kwargs)
	get_place(kwargs)

	pprint(kwargs, sort_dicts=False)


def standart_save_results(**kwargs):
	get_metadata(**kwargs)
