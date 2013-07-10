import urwid
import os
from treetools import *


class ExampleTreeWidget(TreeWidget):
	""" Display widget for leaf nodes """
	def get_display_text(self):
		return self.get_node().get_value()['name']


class ExampleParentWidget(ParentWidget):
	""" Display widget for interior/parent nodes """
	def __init__(self, node):
		# disable expanding by default
		self.__super.__init__(node)

		self.expanded = starts_expanded(node.get_value()["name"])
		self.update_widget()


	def get_display_text(self):
		return self.get_node().get_value()['name']


class ExampleNode(TreeNode):
	""" Data storage object for leaf nodes """
	def load_widget(self):
		return ExampleTreeWidget(self)


class ExampleParentNode(ParentNode):
	""" Data storage object for interior/parent nodes """
	def load_widget(self):
		return ExampleParentWidget(self)

	def load_child_keys(self):
		data = self.get_value()
		return range(len(data['children']))

	def load_child_node(self, key):
		"""Return either an ExampleNode or ExampleParentNode"""
		childdata = self.get_value()['children'][key]
		childdepth = self.get_depth() + 1
		if 'children' in childdata:
			# has children
			if len(childdata["children"]) == 0:
				# must still load children
				print >>open("debug.log", "w"), childdata
				for item in childdata["obj-data"]:
					con = {"name": item.title(), "obj-data": item}
					if(hasattr(item, "__getitem__")):
						# contains iterable content
						con["children"] = []
					childdata["children"].append(con)
			childclass = ExampleParentNode
		else:
			childclass = ExampleNode
		return childclass(childdata, parent=self, key=key, depth=childdepth)


class ExampleTreeBrowser:
	palette = [
			('body', 'black', 'light gray'),
			('selected', 'black', 'dark green', ('bold','underline')),
			('focus', 'light gray', 'dark blue', 'standout'),
			('selected focus', 'yellow', 'dark cyan', 
			('bold','standout','underline')),
			('head', 'yellow', 'black', 'standout'),
			('foot', 'light gray', 'black'),
			('key', 'light cyan', 'black','underline'),
			('title', 'white', 'black', 'bold'),
			('dirmark', 'black', 'dark cyan', 'bold'),
			('flag', 'dark gray', 'light gray'),
			('error', 'dark red', 'light gray'),
		]
	
	footer_text = [
			('title', "Season Browser"), "    ",
			('key', "Have fun")
		]

	def __init__(self, data=None):
		self.topnode = ExampleParentNode(data)
		self.listbox = TreeListBox(TreeWalker(self.topnode))
		self.listbox.offset_rows = 1
		self.header = urwid.Text( "" )
		self.footer = urwid.AttrWrap( urwid.Text( self.footer_text ),
			'foot')
		self.view = urwid.Frame( 
			urwid.AttrWrap( self.listbox, 'body' ), 
			header=urwid.AttrWrap(self.header, 'head' ), 
			footer=self.footer )

	def main(self):
		"""Run the program."""
		
		self.loop = urwid.MainLoop(self.view, self.palette,
			unhandled_input=self.unhandled_input)
		self.loop.run()

		# on exit, write the selected filenames to the console
		names = []
		for node in self.topnode.get_selected_nodes():
			names.append(node.get_value()['name'])
		print '"' + '", "'.join(names) + '"'

	def unhandled_input(self, k):
		if k in ('q','Q'):
			raise urwid.ExitMainLoop()


def get_tree(obj):
	res = {"name": obj.title(), "obj-data": obj}
	if hasattr(obj, "__getitem__"):
		res["children"] = []
		for item in obj:
			con = {"name": item.title(), "obj-data": item}
			if(hasattr(item, "__getitem__")):
				con["children"] = []
			res["children"].append(con)
	return res


import handlers
drwho = handlers.wrap("http://www.btvguide.com/Doctor-Who")


def starts_expanded(val):
	if val == drwho.title():
		return True
	return False


sample = get_tree(drwho)
ExampleTreeBrowser(sample).main()
