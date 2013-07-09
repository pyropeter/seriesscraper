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

