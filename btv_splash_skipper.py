import mechanize
from foo import newBrowser

def get_next_page(url):
	br = newBrowser(url)

	br.select_form("watch_form")
	control = br.form.find_control("submit")

	return br.submit().geturl()
