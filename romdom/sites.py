"""
Classes defining how to query sites for information
"""

import re
import logging
import string
import requests
import urlparse
from romdom import util

logger = logging.getLogger(__name__)


class BaseSite(object):
    """Base class for all RomSites"""

    _LETTERS = '#' + string.ascii_uppercase # not to be modified by subclasses

    _base_url      = '' # the site's FQDN
    _rom_page_url  = '' # {system} {letter} {page}
    _system_url    = '' # the url that the system list can be parsed from. leave empty to use _base_url
    _system_regex  = '' # a regex string used to match systems in the site's html
                        # should contain two groups, one for the system display name,
                        # and another for the system url. use named regex groups
                        # (?P<url>) and (?P<name>)

    @classmethod
    def derived(cls):
        """generates subclasses of this class recursively"""
        for c in cls.__subclasses__():
            yield c
            for sc in c.derived():
                yield sc
        
    @util.cacheable
    def get_systems(self, url=None):
        """return a dictionary of system_names -> url_part"""
        if url is None:
            url = self._base_url
        logger.debug('getting systems from %s', url)
        # TODO: error if page not found
        html = self._get_site_html(page=self._system_url, headers={'Accept-Encoding': ''})
        logger.debug(html)
        return self._find_systems(html)


    def _get_site_html(self, page=None, headers=None):
        url = self._base_url
        if page is not None:
            url = urlparse.urljoin(url, page)
        return requests.get(url, headers=headers if headers is not None else {}).text


    def _find_systems(self, html):
        """uses self._system_regex to find all systems in the html.
        if self._system_regex is not defined, delegates to self._system_matcher"""

        if self._system_regex:
            matcher = re.compile(self._system_regex, re.MULTILINE | re.IGNORECASE)
            pairs = set((m.groupdict()['name'], m.groupdict()['url']) for m in matcher.finditer(html))
            urls = set()
            matches = []
            for p in pairs:
                if p[1] not in urls:
                    matches.append(p)
                    urls.add(p[1])
            return dict(matches)
        else:
            return self._system_matcher(html)


    def _system_matcher(self, html):
        """if matching systems is too complex for a regex, define this function"""
        return []
        

    def _get_letters(self):
        """return a list of 27 elements, corresponding to what this site uses
        to refer to an alphanumeric rom page"""
        return list(self.LETTERS)

    def get_letter_map(self):
        """return a dictionary of standardized letters to site specific letters"""
        letters = self._get_letters()
        return dict(zip(list(self.LETTERS), letters))


class RomHustler(BaseSite):
    _base_url = "http://www.romhustler.net"
    _rom_page_url = "/roms/{system}/{letter}/page:{page}"
    _system_regex = r'<a\s*href="/roms/(?P<url>[^"]*)"[^>]*>(?P<name>[^<]*)</a>'

    def _get_letters(self):
        return ["number"] + list(string.ascii_lowercase)


class DopeRoms(BaseSite):
    _base_url = "http://www.doperoms.com"
    _rom_page_url = "/roms/{system}/{letter}"
    _system_regex = r'<a\s*href="/roms/(?P<url>[^/.]*).html">(?P<name>[^<]*)</a>'


    def _get_letters(self):
        return ["0-9"] + list(string.ascii_uppercase)


class RomWorld(BaseSite):
    _base_url = "http://www.rom-world.com"
    _rom_page_url = "/dl.php?name={system}&letter={letter}"
    _system_regex = r'<a\s*href="/dl\.php\?name=(?P<url>[^"]*)">(?P<name>[^<]*)</a>'


    def _get_letters(self):
        return ["0-9"] + list(string.ascii_uppercase)


class FreeRoms(BaseSite):
    _base_url = "http://freeroms.com"
    _rom_page_url = "/{system}_roms_{letter}.htm"
    _system_regex = r'<a\s*href="http://www\.freeroms\.com/(?P<url>[^.]*)\.htm"\s*>(?P<name>[^<]*)</a>'

    def _get_letters(self):
        return ["NUM"] + list(string.ascii_uppercase)


class RomNation(BaseSite):
    _base_url = "http://romnation.net"
    _system_url = "/srv/roms.html"
    _rom_page_url = "/srv/roms/{system}/{letter}.html"
    _system_regex = r'<a\s*href="/srv/roms/(?P<url>[^.]*)\.html"\s*>(?P<name>.*?) Roms</a>'


    def _get_letters(self):
        return ['0'] + list(string.ascii_uppercase)
