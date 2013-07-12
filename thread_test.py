import threading, time, os, pickle
from threading import Lock
from debugger import log
from Queue import Queue
from random import random

childLock = Lock()

class ChildLoader (threading.Thread):
	def __init__(self, nib, obj, pipe=None):
		threading.Thread.__init__(self)

#		self.nib = nib # node id
#		self.obj = obj # data object (used to load all other nodes)

		self.pipe = pipe

		self.loaded_data = [(nib, obj)]
		self.event_loop = Queue() # contains id of nodes which should be expanded

		log("[THREAD] Initialized " + str(obj) + " at " + str(nib) + " (Pipe: " + str(self.pipe) + ")")

	def run(self):
		while True:
			log("[THREAD] Checking queue")
			cur_id = self.event_loop.get()
			log("[THREAD] Parsing " + str(cur_id))
			children = []
			for (nib, obj) in self.loaded_data:
				if cur_id == nib:
					# lets load needed children
					log("[THREAD] Found needed data")
					for item in obj:
						new_id = random()

						# for gui
						con = {"name": item.title(), "id": new_id}
						if(hasattr(item, "__getitem__")):
							con["children"] = []
						children.append(con)

						# for loader
						self.loaded_data.append((new_id, item))

						log("[THREAD] Appended data: " + str(con))

			# send gui stuff
			log("[THREAD] Writing to pipe: " + str(self.pipe))
			os.write(self.pipe, pickle.dumps((cur_id, children)))

			# lock until data is parsed
			log("[THREAD] Locking myself up")
			childLock.acquire()
			log("[THREAD] Was unlocked")

	def get_children(self, nib):
		log("[THREAD] Added " + str(nib) + " to queue")
		self.event_loop.put(nib)

	def set_pipe(self, new_pipe):
		log("[THREAD] Set pipe to " + str(new_pipe))
		self.pipe = new_pipe
