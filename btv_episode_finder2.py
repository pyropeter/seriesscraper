import mechanize, string, re
from foo import newBrowser

def hups2episodes(hups, base_url):
	seasons = {}
	for hup in hups:
		m = re.match(r"(.*) \(([\d]+)\)", hup)
		name = m.group(1).replace(" ", "+")

		episodes = []
		url = base_url + "season-contents/" + name
		br.open(url)
		cont = br.response().read()

		for link in br.links():
			attrs = {a:b for a,b in link.attrs}
			try:
				if attrs["class"] == "title":
					episodes.append((link.text, attrs["href"]))
			except KeyError:
				pass

		seasons[m.group(1)] = episodes
	return seasons

def get_episodes(url):
	# directly move to episode list
	br = newBrowser(url + "watch-online")

	hups = []
	for link in br.links():
		attrs = {a:b for a,b in link.attrs}
		try:
			if string.find(attrs["href"], "javascript: showSeason") != -1:
				hups.append(link.text)
		except KeyError:
			pass

	return hups2episodes(hups, url)

import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(get_episodes("http://www.btvguide.com/Doctor-Who/"))
