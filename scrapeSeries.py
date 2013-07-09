import re
import os
import sys

from btv_episode_finder import get_episodes
from btv_portal_finder import get_portals
from btv_splash_skipper import get_next_page
import portals

def filenameEscape(name):
	return re.sub(r"[ /\0]", "_", name)

def getStream(urls):
	for url in urls:
		url = get_next_page(url)
		print("Trying: %s" % url)
		stream = portals.scrape(url)
		if stream != None:
			return stream

	raise Exception("No stream found for episode -> fail")

def saveStream(stream, outfile):
	bytesRead = 0
	print "0",

	while True:
		buf = stream.read(10240)
		if not buf:
			break
		bytesRead += len(buf)
		print "\r%i" % bytesRead,
		sys.stdout.flush()
		outfile.write(buf)

	print "\r",

for season, episodes in get_episodes(sys.argv[1]).items():
	if season != "Season 1":
		continue

	print("Season: %s" % season)
	path = filenameEscape(season)

	try:
		os.mkdir(path)
	except OSError as e:
		if e.errno != 17:  # 17: File exists
			raise

	for num, episode in enumerate(episodes):
		print("Episode: %s" % episode)
		name, portalurls = get_portals(episode)
		filename = "%s/%02i-%s" % (path, num + 1, filenameEscape(name))
		stream = getStream(portalurls)
		print("Writing %s" % filename)
		outfile = open(filename, "w")
		saveStream(stream, outfile)
		stream.close()
		outfile.close()

print("Done!")

