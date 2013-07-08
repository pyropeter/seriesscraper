import mechanize, string, re

def get_portals(url):
	br = mechanize.Browser(factory=mechanize.RobustFactory())

	# super useful
	br.set_handle_refresh(False)
	br.set_handle_equiv(False)
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

	# directly move to portal list
	page = br.open(url + "/watch-online")

	# get name
	name = re.search(r"&rarr; ([^<]+)<", br.response().read()).group(1).strip()

	# get portals
	portals = []
	for link in br.links():
		t = link.text
		if t and string.find(t, "EXTERNAL LINK") != -1:
			u = link.url
			if u:
				portals.append(u)

	return name, portals

print get_portals("http://www.btvguide.com/The-Walking-Dead/Season-1/episode-3")
