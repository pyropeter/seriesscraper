import threading, time, os, pickle
from debugger import log

class ChildLoader (threading.Thread):
	def __init__(self, node, pipe):
		threading.Thread.__init__(self)

		self.objdata = node.get_value()['obj-data']
		self.loaded_children = []
		self.pipe = pipe
		self.node = node

		log("[THREAD] Loading children for: " + str(node.get_value()['id']) + " [" + node.get_value()["name"] + "]")

	def run(self):
		for item in self.objdata:
			con = {"name": item.title(), "obj-data": item}
			if(hasattr(item, "__getitem__")):
				con["children"] = []
			self.loaded_children.append(con)
			log("[THREAD] Appended: " + str(con))
		log("[THREAD] Finished loading -> transfering data")
		log("---")
		log(self.loaded_children)
		log("---")
		os.write(self.pipe, pickle.dumps((self.node.get_value()['id'], self.loaded_children)))
