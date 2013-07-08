import mechanize, string, re

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
		seasons[name] = episodes
	return seasons

def get_episodes(url):
	br = mechanize.Browser(factory=mechanize.RobustFactory())

	# super useful
	br.set_handle_refresh(False)
	br.set_handle_equiv(False)
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

	# directly move to episode list
	page = br.open(url + "watch-online")

	hups = []
	for link in br.links():
		attrs = {a:b for a,b in link.attrs}
		try:
			if string.find(attrs["href"], "javascript: showSeason") != -1:
				hups.append(link.text)
		except KeyError:
			pass

	return hups2episodes(hups, url)

