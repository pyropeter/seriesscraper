import mechanize, string, re
from foo import newBrowser

def get_portals(url):
	# directly move to portal list
	br = newBrowser(url + "/watch-online")

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
