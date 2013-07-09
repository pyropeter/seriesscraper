import string, re, urlparse, urllib
from foo import NotMyDepartmentException, newBrowser

def get_seasons(url):
	br = newBrowser("%s/watch-online" % url.rstrip("/"))
	items = []
	for se_link in br.links():
		attrs = {a:b for a, b in se_link.attrs}
		try:
			if string.find(attrs["href"], "javascript: showSeason") != -1:
				season = re.match(r"(.*) \(([\d]+)\)", se_link.text).group(1)
				items.append((season, "%s/season-contents/%s" % (url.rstrip("/"), urllib.quote_plus(season))))
		except KeyError:
			pass
	return items

def get_alternatives(url):
	print "%s/watch-online" % url.rstrip("/")
	br = newBrowser("%s/watch-online" % url.rstrip("/"))
	streamers = []
	for link in br.links():
		attrs = {a:b for a, b in link.attrs}
		try:
			if attrs["class"] == "title":
				streamers.append((link.text, attrs["href"]))
		except KeyError:
			pass
	return streamers

def get_episodes(url):
	print "get episode"

def scrape(url):
	res = []

	print "scrape"
	# detect url type
	if re.match(r"http://www.btvguide.com/[^/]+/season-contents/.+", url):
		# get season
		res = get_episodes(url)
	elif re.match(r"http://www.btvguide.com/[^/]+/[^/]/episode.+", url):
		# get episode
		res = get_alternatives(url)
	else:
		# get series
		res = get_seasons(url)

	return (res, True, False, False)
