import mechanize

class NotMyDepartmentException(Exception):
	pass

def newBrowser(url=None):
	br = mechanize.Browser(factory=mechanize.RobustFactory())

	# don't do stuff we don't need anyway
	br.set_handle_refresh(False)
	br.set_handle_equiv(False)
	br.set_handle_robots(False)

	if url != None:
		br.open(url)

	return br

class Thingie(object):
	def __init__(self, url, title=None):
		self._url = url
		self._fetched = False
		self._title = title

	def title(self):
		if self._title == None:
			self.fetch()
		return self._title

class ThingieWithItems(Thingie):
	def __len__(self):
		self.fetch()
		return self._items.__len__()

	def __getitem__(self, key):
		self.fetch()
		return self._items.__getitem__(key)

	def __iter__(self):
		self.fetch()
		return self._items.__iter__()
