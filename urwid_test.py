import urwid
import os
from random import random
from treetools import *
from thread_test import *
from debugger import log
from threading import Lock


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
			childLoader.get_children(data["id"])

			self.get_widget().loading = True
			self.get_widget().update_widget()

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

	def add_child(self, name, nib, children=None):
		try:
			con = {"name": name, "id": nib}
			if children != None:
				con["children"] = children
			self.get_value()["children"].append(con)

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
			('key', "Press [h] for help")
		]

	def __init__(self, data=None, title=None):
		self.topnode = ExampleParentNode(data)
		self.listbox = TreeListBox(TreeWalker(self.topnode))
		self.listbox.offset_rows = 1

		self.header_text = [
			('title', "Series:"), "    ",
			('key', title)
		]

		self.header = urwid.AttrWrap(urwid.Text(self.header_text), 'head')
		self.footer = urwid.AttrWrap(urwid.Text(self.footer_text), 'foot')

		self.view = urwid.Frame( 
			urwid.AttrWrap( self.listbox, 'body' ), 
			header=urwid.AttrWrap(self.header, 'head' ), 
			footer=self.footer )

	def main(self):
		"""Run the program."""
		
		self.loop = urwid.MainLoop(self.view, self.palette,
			unhandled_input=self.unhandled_input)
		# handle threaded loading
		childLoader.set_pipe(self.loop.watch_pipe(self.say_hello))
		childLoader.start()

		self.loop.run()

	def unhandled_input(self, k):
		if k in ('q','Q'):
			raise urwid.ExitMainLoop()
		elif k in ('h', 'H'):
			log("[GUI] Not implemented yet")
		elif k in ('w', 'W'):
			log("[GUI] Going to watch selected stream")
			node = self.find_select(self.topnode)
			log(node)
			childLoader.watch_stream(node.get_data()["id"])

	def say_hello(self, data):
		# callback method when some children were loaded
		log("[GUI] Received data")
		parent_id, children_data = pickle.loads(str(data))
		log("[GUI] Parsed data")

		node = self.find_node(self.topnode, parent_id)
		log("[GUI] Traced node")
		for c in children_data:
			if "children" in c:
				node.add_child(c["name"], c["id"], c["children"])
			else:
				node.add_child(c["name"], c["id"])
		log("[GUI] Added all children")

		node.get_widget().loading = False
		node.get_widget().update_widget()

		log("[GUI] Unlocking thread")
		childLock.release()

	def find_node(self, cur_node, nid):
		data = cur_node.get_value()
		if data["id"] == nid:
			return cur_node
		if "children" in data:
			if len(data["children"]) > 0:
				ns = []
				for i in cur_node.load_child_keys():
					ns.append(cur_node.get_child_node(i))
				for c in ns:
					n = self.find_node(c, nid)
					if n != None:
						return n
			else:
				log("[GUI] Wrong ID and no children -> abort")
		else:
			log("[GUI] No more children -> abort")

	def find_select(self, cur_node):
		# stupid copy paste
		data = cur_node.get_value()
		log(data["name"])
		log(cur_node.get_widget().selected)
		log("---")
		if cur_node.get_widget().is_selected():
			return cur_node
		if "children" in data:
			if len(data["children"]) > 0:
				ns = []
				for i in cur_node.load_child_keys():
					ns.append(cur_node.get_child_node(i))
				for c in ns:
					n = self.find_select(c)
					if n != None:
						return n
			else:
				log("[GUI] Wrong ID and no children -> abort")
		else:
			log("[GUI] No more children -> abort")
		
# my pipe
import os, pickle
pipe = None

head_title = ""
def get_tree(obj):
	global head_title, pipe 
	head_title = obj.title()

	res = {"name": obj.title(), "id": random(), "children": []}

	loader = ChildLoader(res["id"], obj, pipe)
	loader.daemon = True

	return loader, res


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


childLoader, sample = get_tree(drwho)
ExampleTreeBrowser(sample, title=head_title).main()
