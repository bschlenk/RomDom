"""
Urls
"""

from urlparse import urljoin


def _create_url_class(name, base, rom, download):
    members = {
        'base_url': base,
        'rom_url': urljoin(base, rom),
        'download_url': urljoin(base, download),
    }
    return type(name, (object,), members)
    
        
Coolrom = _create_url_class(
    'Coolrom',
    'http://coolrom.com',
    'roms',
    'dlpop.php?id={id}'
)

#Romhustler = _create_url_class(
#    'Romhustler',
#    'http://romhustler.net',
#    'roms',
#)
