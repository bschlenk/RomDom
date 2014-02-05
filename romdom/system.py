"""
CoolromSystem classes - class used to iterate over all of the roms for a given system
"""

import urlparse
import string
import re

from romdom import util
from romdom.rom import Rom

class SystemError(Exception):
	pass

class System(object):
	"""Class for browsing roms of a particular system"""
	pages = list('0' + string.ascii_lowercase)

	def __init__(self, system, url):
		self.system_name = system
		self.url = url
		
	def __str__(self):
		return self.system_name
		
	def __repr__(self):
		return '<System: %s (%s)>' % (self.system_name, self.url)
		
	def get_page_url(self, page):
		"""Get the url of the letter page"""
		return '%s/' % urlparse.urljoin(self.url, page)
		
	def get_page_urls(self):
		"""Get a list of urls that roms for this system can be found at"""
		return map(self.get_page_url, System.pages)
		
	@util.cacheable
	def get_rom_list(self, page):
		"""Get a list of roms for a given page"""
		print 'getting rom page %s' % page
		url = self.get_page_url(page)
		html = util.get_html(url)
		matcher = re.compile(r'<a href="(/roms/%s/\d*?/[^<>]*?.php)">\s*(?!<img)([^<>]*?)</a>' % self.url.rsplit('/', 2)[-2])
		matches = matcher.findall(html)
		return [Rom(m[1], urlparse.urljoin(self.url, m[0])) for m in matches]
		
	def get_all_roms(self):
		"""Get a list of all roms for this system"""
		roms = []
		for p in System.pages:
			roms.extend(self.get_rom_list(p))
		return roms
		
	def get_rom(self, rom_name):
		if rom_name[0].lower() in string.ascii_lowercase:
			roms = self.get_rom_list(rom_name[0].lower())
		else:
			roms = get_rom_list('0')
		for r in roms:
			if rom_name == r:
				return r
		return None
		
	def search(self, query):
		"""Search through all this system's roms for roms containing the query"""
		results = []
		for rom in self.get_all_roms():
			if query.lower() in str(rom).lower():
				results.append(rom)
		return results
		
		
