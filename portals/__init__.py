import os
import importlib
from foo import NotMyDepartmentException

portals = []

for module in os.listdir(os.path.dirname(__file__)):
	if module == '__init__.py' or module[-3:] != '.py':
		continue
	portals.append(importlib.import_module("portals.%s" % module[:-3]))

def scrape(url):
	for portal in portals:
		try:
			return portal.scrape(url)
		except NotMyDepartmentException:
			pass

