from foo import NotMyDepartmentException
import re
import urllib
import mechanize

def scrape(url):
	if not re.match(r"http://gorillavid.in/[a-z0-9]+", url):
		raise NotMyDepartmentException()

	return urllib.urlopen(getStreamUrl(url))

def getStreamUrl(url):
	br = mechanize.Browser(factory=mechanize.RobustFactory())
	# don't do stuff we don't need anyway
	br.set_handle_refresh(False)
	br.set_handle_equiv(False)
	br.set_handle_robots(False)

	# open the first page
	br.open(url)

	# push the big red button
	br.select_form(nr=1)
	br.submit()

	# now it gets ugly
	html = br.response().read()
	return re.search(r"file: \"([^\"]+)\"", html).group(1)

