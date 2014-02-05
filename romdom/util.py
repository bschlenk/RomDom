"""
RomDom utility functions
"""

import urllib2
import functools

def get_html(site):
	"""Returns the HTML of the given url"""
	req = urllib2.urlopen(site)
	return req.read()
	
class Cacheable:
	"""My original attempt at a cacheing wrapper. Doesn't work on member functions"""
	def __init__ (self, f):
		self.f = f
		self.mem = {}
		
	def __call__ (self, *args, **kwargs):
		key = (args, str(kwargs))
		if key in self.mem:
			return self.mem[key]
		else:
			tmp = self.f(*args, **kwargs)
			self.mem[key] = tmp
			return tmp
		
def cacheable(func):
	"""Cache the return value of func based on the input arguments"""
	@functools.wraps(func)
	def inner(*args, **kwargs):
		key = (args, str(kwargs))
		if key in inner.mem:
			return inner.mem[key]
		else:
			tmp = func(*args, **kwargs)
			inner.mem[key] = tmp
			return tmp
	inner.mem = {}
	return inner
