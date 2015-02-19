"""
Coolrom Rom class - the representation of a game rom
"""

import sys
import requests
import re
from romdom import util
from romdom import urls

class RomError(Exception):
    pass

class Rom(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url
            
    def __str__(self):
        return self.name
            
    def __repr__(self):
        return '<Rom: %s (%s)>' % (self.name, self.url)
            
    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, Rom):
            return self.name == other.name
        raise ValueError('Rom cannot be compared to %s' % str(type(other)))
            
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def download(self, save_as=None):
        if not save_as:
            save_as = '%s.zip' % self.name
        num = re.match(r'^%s.*?/(\d*)/%s$' % (urls.COOLROM_ROMS, self.url.rsplit('/', 1)[-1]), 
                self.url).group(1)
        url = urls.COOLROM_DOWNLOAD_POPUP.format(id=num)
        html = util.get_html(url)
        matcher = re.compile(r'Please click below to download.*?<form method="POST" action="([^<>]*?)">')
        match = matcher.search(html)
        download_url = match.group(1)
        headers = {
                'Connection': 'keep-alive',
                'Host': 'fs2.coolrom.com',
                'Origin': 'http://coolrom.com',
                'Referer': url
        }
        r = requests.post(download_url, headers=headers, stream=True)
        if r.status_code == 200:
            try:
                length = int(r.headers.get('content-length'))
            except ValueError:
                length = 0
            total = 0
            print
            with open(save_as, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)
                    total += len(chunk)
                    sys.stdout.write('\rDownloading "%s" -> "%s"... %3d%%' % (self.name, save_as, 100 * float(total)/length))
            print
    
