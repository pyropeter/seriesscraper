import portals

# this will work as long the video isn't deleted. ah, well...
assert len(portals.scrape("http://gorillavid.in/ajb5k209eo85").read(1024)) == 1024
