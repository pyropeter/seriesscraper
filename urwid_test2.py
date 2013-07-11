import urwid
import os
from random import random
from treetools import *
from thread_test2 import *
from debugger import log


class ExampleTreeWidget(TreeWidget):
	""" Display widget for leaf nodes """
	def get_display_text(self):
		return self.get_node().get_value()['name']


class ExampleParentWidget(ParentWidget):
	""" Display widget for interior/parent nodes """
	def __init__(self, node):
		self.__super.__init__(node)

		self.expanded = starts_expanded(node.get_value()["name"])
		self.loading = False

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

		if len(data['children']) == 0:
			# must still load children for this node
			loader = ChildLoader(self, pipe)
			loader.start()
			self.get_widget().loading = True
			self.get_widget().update_widget()

#			for item in data['obj-data']:
#				con = {"name": item.title(), "obj-data": item}
#				if(hasattr(item, "__getitem__")):
					# contains iterable content
#					con["children"] = []
#				data['children'].append(con)
#					self.add_child(con["name"], con["children"], con["obj-data"])
#				else:
#					self.add_child(con["name"])

		return range(len(data['children']))

	def load_child_node(self, key):
		"""Return either an ExampleNode or ExampleParentNode"""
		childdata = self.get_value()['children'][key]
		childdepth = self.get_depth() + 1
		if 'children' in childdata:
			childclass = ExampleParentNode
		else:
			childclass = ExampleNode
		return childclass(childdata, parent=self, key=key, depth=childdepth)

	def add_child(self, name, children=None, objdata=None):
		try:
			con = {"name": name, "id": random()}
			if children != None and objdata != None:
				con["children"] = children
				con["obj-data"] = objdata
			self.get_value()["children"].append(con)
			log("Added child: " + str(con))
			self.new_children_loaded = True
			self.get_widget().update_widget()
		except KeyError:
			pass


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

	def __init__(self, data=None, title=None):
		self.topnode = ExampleParentNode(data)
		self.listbox = TreeListBox(TreeWalker(self.topnode))
		self.listbox.offset_rows = 1

		self.header_text = [
			('title', "Series:"), "    ",
			('key', title)
		]

		self.header = urwid.AttrWrap( urwid.Text( self.header_text ), 'head')
		self.footer = urwid.AttrWrap( urwid.Text( self.footer_text ), 'foot')

		self.view = urwid.Frame( 
			urwid.AttrWrap( self.listbox, 'body' ), 
			header=urwid.AttrWrap(self.header, 'head' ), 
			footer=self.footer )

	def main(self):
		"""Run the program."""
		
		self.loop = urwid.MainLoop(self.view, self.palette,
			unhandled_input=self.unhandled_input)
		# handle threaded loading
		global pipe
		pipe = self.loop.watch_pipe(self.say_hello)

		self.loop.run()

	def unhandled_input(self, k):
		if k in ('q','Q'):
			raise urwid.ExitMainLoop()
		elif k in ('w', 'W'):
			self.add_node(self.topnode, "Ich bin neu hier")
			self.topnode.add_child("moin")

	def say_hello(self, data):
		# callback method when some children were loaded
		log("Pickle through data now!")
		node_id, children = pickle.loads(str(data))
		log("Pickle complete, looking for: " + str(node_id))
		node = self.find_node(self.topnode, node_id)
		log("Adding children to " + node.get_value()["name"])
		for c in children:
			node.add_child(c["name"], c["children"], c["obj-data"])
		node.get_widget().loading = False
		node.get_widget().update_widget()

	def find_node(self, cur_node, nid):
		data = cur_node.get_value()
		log("Comparing IDs: " + str(data["id"]) + " [" + data["name"] + "] vs " + str(nid))
		if data["id"] == nid:
			log("Found id: " + str(cur_node))
			return cur_node
		if len(data["children"]) > 0:
			ns = []
			log("Goind to load keys")
			for i in cur_node.load_child_keys():
				ns.append(cur_node.get_child_node(i))
			log("Keys loaded")
			for c in ns:
				n = self.find_node(c, nid)
				if n != None:
					return n
		else:
			log("Wrong ID and no children -> abort")
		

	def add_node(self, node, name):
		node.get_value()["children"].append({"name": name, "id": random()})
		node.new_children_loaded = True
		node.get_widget().update_widget()

# my pipe
import os, pickle
pipe = None

head_title = ""
def get_tree(obj):
	global head_title 
	head_title = obj.title()
	res = {"name": obj.title(), "obj-data": obj, "id": random()}
	if hasattr(obj, "__getitem__"):
		res["children"] = []
		for item in obj:
			con = {"name": item.title(), "obj-data": item, "id": random()}
			if(hasattr(item, "__getitem__")):
				con["children"] = []
			res["children"].append(con)
	return res


import handlers
import sys
if len(sys.argv) > 1:
	drwho = handlers.wrap("http://www.btvguide.com/%s" % " ".join(sys.argv[1:]).replace(" ", "-"))
else:
	drwho = handlers.wrap("http://www.btvguide.com/Doctor-Who")


def starts_expanded(val):
	if val == head_title:
		return True
	return False


sample = get_tree(drwho)
ExampleTreeBrowser(sample, title=head_title).main()
