import mechanize, string, re
from foo import newBrowser

def hups2episodes(hups, base_url):
	seasons = {}
	for hup in hups:
		m = re.match(r"(.*) \(([\d]+)\)", hup)
		name = m.group(1).replace(" ", "-")
		num = int(m.group(2))

		episodes = []
		for i in range(1, num + 1):
			url = base_url + name + "/" + "episode-" + str(i)
			episodes.append(url)
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

