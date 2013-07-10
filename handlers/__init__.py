import os
import importlib
from foo import NotMyDepartmentException

handlers = []

for module in os.listdir(os.path.dirname(__file__)):
	if module == '__init__.py' or module[-3:] != '.py':
		continue
	handlers.append(importlib.import_module("handlers.%s" % module[:-3]))

def wrap(url):
	for handler in handlers:
		try:
			return handler.wrap(url)
		except NotMyDepartmentException:
			pass

