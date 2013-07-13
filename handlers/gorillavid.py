from foo import NotMyDepartmentException, newBrowser, Thingie
import re, urllib, mechanize

def wrap(url):
	if not re.match(r"http://gorillavid.in/[a-z0-9]+", url):
		raise NotMyDepartmentException()

	return Stream(url)

class Stream(Thingie):
	def __init__(self, url):
		Thingie.__init__(self, url, url)

	def stream(self):
		# open the first page
		br = newBrowser(self._url)

		# push the big red button
		br.select_form(nr=1)
		br.submit()

		# now it gets ugly
		html = br.response().read()
		url = re.search(r"file: \"([^\"]+)\"", html).group(1)
		return urllib.urlopen(url)

	def watch(self):
		fd = self.stream()
		# pipe me into mplayer please!
