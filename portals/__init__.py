import os
import importlib
from foo import NotMyDepartmentException

portals = []

for module in os.listdir(os.path.dirname(__file__)):
	if module == '__init__.py' or module[-3:] != '.py':
		continue
	portals.append(importlib.import_module("portals.%s" % module[:-3]))

def scrape(url):
	""" Scapes the portal url pointing to a playlist-thingie

	return format: (items, containsLists, containsAlternatives, orderMatters)
	items: The items (streams or playlist-thingies) from the portal page
			each item is a tuple: (title, url)
			where title is an informational title for the url (should be an
			human-readable string)
	containsLists: Wether the items are streams or playlist-thingies
	containsAlternatives: If True, every item is a playlist of streams
			containing the same contents.
	orderMatters: If the order of the items should be preserved (e.g.
			by prefixing the filenames with numbers)
	"""
	for portal in portals:
		try:
			return portal.stream(url)
		except NotMyDepartmentException:
			pass

