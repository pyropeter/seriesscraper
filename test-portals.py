import portals

items, containsLists, containsAlternatives, orderMatters = portals.scrape(
		"http://www.btvguide.com/Doctor-Who")
assert containsLists == True
assert containsAlternatives == False
assert orderMatters == False
assert len(items) == 8
assert ("Season 1", "http://www.btvguide.com/Doctor-Who/season-contents/Season+1/") in items
assert ("Season 2", "http://www.btvguide.com/Doctor-Who/season-contents/Season+2/") in items
assert ("Season 3", "http://www.btvguide.com/Doctor-Who/season-contents/Season+3/") in items
assert ("Season 4", "http://www.btvguide.com/Doctor-Who/season-contents/Season+4/") in items
assert ("Season 5", "http://www.btvguide.com/Doctor-Who/season-contents/Season+5/") in items
assert ("Season 6", "http://www.btvguide.com/Doctor-Who/season-contents/Season+6/") in items
assert ("Season 7", "http://www.btvguide.com/Doctor-Who/season-contents/Season+7/") in items
assert ("Special", "http://www.btvguide.com/Doctor-Who/season-contents/Special/") in items

