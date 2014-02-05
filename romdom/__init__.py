import re
import urlparse
from romdom import util
from romdom import urls
from romdom.system import System

def get_system_list():
	html = util.get_html(urls.COOLROM_ROMS)
	matcher = re.compile(r'<a href="(/roms/.*?/)">(.*?)</a>')
	replacer = re.compile(r'<(.*?)\s*.*?>.*?</\1>')
	matches = matcher.findall(html)
	vals = [(replacer.sub('', m[1]).strip(), urlparse.urljoin(urls.COOLROM, m[0])) for m in matches]
	return dict([(s[0], System(*s)) for s in vals])
