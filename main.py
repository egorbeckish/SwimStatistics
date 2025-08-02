import regex
import pdfplumber


p = r"(?<place>[\d]{1,})\s(?<lane>[\d]{1})\s(?<surname>[\S]*)\s(?<name>[\D]*)\s(?<country>[A-Z]{3})\s(?<reaction_time>[\d]{1}\.[\d]{2})\s(?<finish_time>([\d]{1,2}\:)?[\d]{2}\.[\d]{2})(\s(?<behind_time>[\d]{1,2}\.[\d]{2}))?"
path = fr"E:\Telegram\SwimStatistics\contest\University\2025\Rhine-Ruhr (GER)\100m butterfly Men's Final.pdf"

with pdfplumber.open(path) as f:
	f = "\n".join([page.extract_text() for page in f.pages])


#(?<place>[\d]{1,})
#\s
#(?<heat_number>[\d]{1,})?\s?
#(?<lane>[\d]{1})
#\s
#(?<surname>[\S]*)
#\s
#(?<name>[\D]*)
#\s
#(?<country>[A-Z]{3})
#\s
#(?<birthday>[\d]{1,2}\s[A-Z]{3}\s[\d]{4}\s)?
#(?<reaction_time>[\d]{1}\.[\d]{2})
#\s
#(?<split>([\d]{1,2}\:)?[\d]{2}\.[\d]{2})
#\s
#(?<finish_time>([\d]{1,2}\:)?[\d]{2}\.[\d]{2})
#\s?(?<behind_time>[\d]{1,2}\.[\d]{2})?