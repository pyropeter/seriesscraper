import handlers, sys

drwho = handlers.wrap("http://www.btvguide.com/Doctor-Who")

print drwho.title()

for season in drwho:
	print "    " + season.title()

	for episode in season:
		print "        " + episode.title()
#		episode.watch()
		episode.download()

