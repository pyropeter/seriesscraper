from foo import NotMyDepartmentException, newBrowser
import re
import urllib
import mechanize

def scrape(url):
	if not re.match(r"http://gorillavid.in/[a-z0-9]+", url):
		raise NotMyDepartmentException()

	return urllib.urlopen(getStreamUrl(url))

def getStreamUrl(url):
	# open the first page
	br = newBrowser(url)

	# push the big red button
	br.select_form(nr=1)
	br.submit()

	# now it gets ugly
	html = br.response().read()
	return re.search(r"file: \"([^\"]+)\"", html).group(1)

