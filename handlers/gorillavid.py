from foo import NotMyDepartmentException, newBrowser, Thingie
import re, urllib, mechanize

class Stream(Thingie):
	def __init__(self, url, title=None):
		Thingie.__init__(self, url, title)

		# change me later
		self._title = url

	def stream(self, url):
		if not re.match(r"http://gorillavid.in/[a-z0-9]+", url):
			raise NotMyDepartmentException()

		return urllib.urlopen(getStreamUrl(url))

	def getStreamUrl(self, url):
		# open the first page
		br = newBrowser(url)

		# push the big red button
		br.select_form(nr=1)
		br.submit()

		# now it gets ugly
		html = br.response().read()
		return re.search(r"file: \"([^\"]+)\"", html).group(1)
