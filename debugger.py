#import logging

#logging.basicConfig(filename='debug.log',level=logging.DEBUG)



debug = open("debug.log", "w")

def log(msg):
	global debug
	print >> debug, msg
	debug.flush()
