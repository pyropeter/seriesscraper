from foo import NotMyDepartmentException, Thingie, ThingieWithItems, newBrowser
import re
from bs4 import BeautifulSoup
import urllib
import handlers

def wrap(url):
	if re.match(r"http://www.btvguide.com/[^/]+", url):
		return Series(url)
	if re.match(r"http://www.btvguide.com/[^/]+/[^/]+/[^/]+", url):
		return Episode(url)

	raise NotMyDepartmentException

class Series(ThingieWithItems):
	def fetch(self):
		if self._fetched:
			return
		self._fetched = True

		soup = BeautifulSoup(urllib.urlopen("%s/episodes" % self._url))

		# read title
		self._title = soup.h1.text.strip()

		# find seasons
		self._items = []
		seasonfilter = soup.find_all('div', class_='season_filter')[0]
		seasonlinks = seasonfilter.find_all(
				href=lambda x: False if x == None else x.startswith('javascript: showSeason'))
		for link in seasonlinks:
			name = link.strong.text.strip()
			url = "%s/season-contents/%s" % (self._url, urllib.quote_plus(name))
			self._items.append(Season(url, name))

class Season(ThingieWithItems):
	def fetch(self):
		if self._fetched:
			return
		self._fetched = True

		# since there is no easy way to get the season name without additional requests,
		# bail out if the season name isn't already known (set by Series at creation of this object)
		if self._title == None:
			raise Exception("Season thingies have to be created by Series thingies")

		# find episodes
		# there are 30 episodes per page. bail out after 30 pages (900 episodes)
		self._items = []
		for pagenum in range(1, 31):
			soup = BeautifulSoup(urllib.urlopen("%s?page=%i" % (self._url, pagenum)))

			for link in soup.find_all('a', class_='title'):
				name = link.text.strip()
				url = link.attrs['href'].encode('ascii')
				self._items.append(Episode(url, name))

			if not soup.find_all('a', class_='load-more'):
				break
		else:
			raise Exception("More than 30 pages?!")

class Episode(ThingieWithItems):
	def fetch(self):
		if self._fetched:
			return
		self._fetched = True

		soup = BeautifulSoup(urllib.urlopen("%s/watch-online" % (self._url)))

		self._title = soup.find_all('p',
				text=lambda x: False if x == None else x.startswith(u'\u2192'))[0].text[5:].strip()

		self._items = []
		for link in soup.find_all('a', class_='clickfreehoney'):
			if not u'Free Honey' in link.text:
				continue
			name = re.sub(ur'[^\w.]+', ' ', link.text.strip())
			url = link.attrs['href'].encode('ascii')
			self._items.append(StreamWrapper(url, name))

	def stream(self):
		self.fetch()

		for stream in self._items:
			if hasattr(stream, 'stream'):
				return stream.stream()

		raise Exception("No useable stream found")

class StreamWrapper(object):
	def __init__(self, url, title):
		self.__url = url
		self.__title = title
		self.__wrappee = None

	def title(self):
		return self.__wrappee.title() if self.__wrappee else self.__title

	def __getattr__(self, name):
		if not self.__wrappee:
			# fetch wrappee
			br = newBrowser(self.__url)
			br.select_form("watch_form")
			url = br.submit().geturl()
			self.__wrappee = handlers.wrap(url)

		return getattr(self.__wrappee, name)


