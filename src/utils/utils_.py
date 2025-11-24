from lib import (
	datetime,
	bs4,
	iso3166,
	re,
	regex,
	os,
	requests
)


def month_to_int():
	return {datetime.datetime(1970, month, 1).strftime("%B"): month for month in range(1, 13)}


def get_omega_contest(html: bs4.BeautifulSoup):
	return html.find("h1").text


def get_country(alpha3, city=None):
	standart = iso3166.countries[alpha3]
	return {
		"alpah3": alpha3, 
		"country": standart.name,
		"city": city,
		"country_n": standart.numeric
	}


def get_omega_metadata(html: bs4.BeautifulSoup):
	contest = get_omega_contest(html)
	metadata = html.find("p", class_="subtitle").text
	metadata = re.match(r"(?P<month>[a-zA-Z]+)\s(?P<date>(?P<start>[\d]{1,2})[a-zA-Z]{2}\sto\s(?P<month2>[a-zA-Z]+\s)?(?P<end>[\d]{1,2})[a-zA-Z]{2})\s(?P<year>[\d]{4})\s\-\s(?P<city>[a-zA-Z]+)\,\s(?P<country>[a-zA-Z]{3,})", metadata).groupdict()

	year = int(metadata["year"])
	month = month_to_int()[metadata["month"]]
	start = datetime.date(
		year,
		month,
		int(metadata["start"])
	)

	if metadata["month2"]:
		month = month_to_int()[metadata["month2"]]

	end = datetime.date(
		year,
		month,
		int(metadata["end"])
	)
	
	country = get_country(metadata["country"], metadata["city"])
	metadata = {
		"contest": contest,
		"year": year,
		"start": start,
		"end": end,
	}

	metadata.update(country)
	return metadata


def get_days(html: bs4.BeautifulSoup):
	days = html.find_all("div", class_="block-table")
	return {
		"count_days": len(days),
		"days": days
	}


def make_dir(path):
	os.makedirs(path, exist_ok=True)


def save_omega_results(url, pool):
	response = requests.get(url).text
	html = bs4.BeautifulSoup(response, "html.parser")
	metadata = get_omega_metadata(html)
	save_path = fr"{metadata["contest"]}\{pool}\{metadata["year"]}\{pool}"
	make_dir(save_path)

	days = get_days(html)["days"]
	for day in days:
		for challenge in day.find_all("div", class_="row")[2:]:
			try:
				title = challenge.find("p", class_="round").text
				event = re.search(r"(?P<sex>[a-zA-Z]+\'s)\s(?P<style>Freestyle|Backstroke|Butterfly|Breaststroke|Medley)\s(?P<distance>[\d]{2,4}m)\s+((Slowest|Fastest)\s)?(?P<stage>Heats|Semi-finals|Final)(?P<rerun>\sSwim-off)?", title).groupdict()
				if event["rerun"] is None:
					if event["stage"] == "Semi-finals":
						event["stage"] = "Semifinals"
					
					event["style"] = event["style"].lower()
					if event["style"] == "medley":
						event["style"] = "IM"

					event = f"{event["distance"]} {event["style"]} {event["sex"]} {event["stage"]}"
					link = "https://www.omegatiming.com" + challenge.find_all("a")[1]["href"]

					response = requests.get(link).content
					
					with open(fr"{save_path}\{event}.pdf", "wb") as pdf:
						pdf.write(response)
					
			
			except Exception as e:
				# print(e)
				pass


def check_regex(pattern, text):
	pattern = "".join(pattern.split())

	for v in regex.finditer(pattern, text):
		print(v.capturesdict())


# path = r"D:/Self Project/SwimStatistics/contest/Olympic Games/2024"


# view_format = st.selectbox("format", ["pdf", "csv"])

# match view_format:
# 	case "pdf":
# 		file = st.selectbox("file", os.listdir(f"{path}/{view_format}"), None)
# 		view_pdf = st.checkbox("pdf")
# 		if file:
# 			if view_pdf:
# 				with open(fr"{path}/{view_format}/{file}", "rb") as file:
# 					base64_pdf = base64.b64encode(file.read()).decode("utf-8")

# 				pdf_display = f"""
# 					<iframe src="data:application/pdf; base64,{base64_pdf}" 
# 						width="100%" 
# 						height="800px" 
# 						style="border: none;">
# 					</iframe>
# 				"""

# 				st.markdown(pdf_display, unsafe_allow_html=True)
			
# 			else:
# 				text = ""
# 				with pdfplumber.open(fr"{path}/{view_format}/{file}") as f:
# 					for page in f.pages:
# 						text += f"{page.extract_text()}/n"

# 				text = regex.sub(r"/s/(/=?[/d]{1,}/)|/s([/d]{2,}m)", "", text)
# 				st.code(text)
	
# 	case "csv":
# 		st.write("In process...")


# with open(f"{path}/parse.json") as json_file:
# 	json_file = json.load(json_file)

# swimmers = {}
# swimmers_columns = ["place", "lane", "reaction_time", "finish_time", "behind_time", "split"]
# for file in os.listdir(f"{path}/pdf"):
# 	distance, style, stage = re.search(r"([\d]{2,})m\s(\D+)\s\D+(Final|Semifinals|Heats)", file).groups()

# 	file_text = ""
# 	with pdfplumber.open(fr"{path}/pdf/{file}") as f:
# 		for page in f.pages:
# 			file_text += f"{page.extract_text()}/n"

# 	file_text = regex.sub(r"\s\(\=?[\d]{1,}\)|\s([\d]{2,}m)", "", file_text)

# 	if stage == "Final":
# 		columns = ["place", "lane", "fullname", "country", "reaction_time", "finish_time", "behind_time", "split"]
# 	else:
# 		columns = ["place", "heats", "lane", "fullname", "country", "reaction_time", "finish_time", "behind_time", "split"]

# 	if distance == "50":
# 		columns.pop(-1)

# 	data = []
# 	for val in regex.finditer(json_file[distance], file_text):
# 		val = val.capturesdict()

# 		[swimmer] = val["fullname"]

# 		if not val["behind_time"]:
# 			val["behind_time"] = [""]
		
# 		if "split" in val:
# 			val["split"] = [" ".join(val["split"])]

# 		if swimmer not in swimmers:
# 			swimmers[swimmer] = {
# 				"metadata": {
# 					"country": "",
# 					"birthday": ""
# 				},
# 				"events": []
# 			}

# 		if stage == "Heats":
# 			[country] = val["country"]
# 			[birthday] = val["birthday"]

# 			swimmers[swimmer]["metadata"]["country"] = country
# 			swimmers[swimmer]["metadata"]["birthday"] = birthday 

# 		result = [val[k][0] for k in columns]
# 		data += [result]

# 		swimmer_event = {
# 			"event": {
# 				"distance": distance,
# 				"style": style,
# 				"stage": stage,
# 			}
# 		}
# 		swimmer_event.update({k: val[k][0] for k in (swimmers_columns if "split" in val else swimmers_columns[:-1])})
# 		swimmers[swimmer]["events"] += [swimmer_event]

# 	pd.DataFrame(data, columns=columns).to_csv(
# 		f"{path}/csv/results/{file.replace("pdf", "csv", 1)}",
# 		index=False
# 	)

# for k, v in swimmers.items():
# 	with open(f"{path}/csv/swimmers/{k}.json", "w") as f:
# 		f.write(json.dumps(v, indent=4))