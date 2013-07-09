import os
import importlib
from foo import NotMyDepartmentException

hosters = []

for module in os.listdir(os.path.dirname(__file__)):
	if module == '__init__.py' or module[-3:] != '.py':
		continue
	hosters.append(importlib.import_module("hosters.%s" % module[:-3]))

def stream(url):
	for hoster in hosters:
		try:
			return hoster.stream(url)
		except NotMyDepartmentException:
			pass

