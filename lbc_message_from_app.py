from termios import VT1
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import etree
import re
import logging
import urllib.parse
import os.path
from enum import Enum
from lbc_message import MESSAGE_STRUCT
class LbcMessageFromApp:
    def __init__(self):
        self.link_finder_re = re.compile('.*(https://www.leboncoin.fr/ventes_immobilieres/.+\.htm).*')
        self.finder = None
        self.date = None
        self.content = None
    def loadFromFile(self, file):
        self.date = os.path.getmtime(file)
        with open(file, 'r') as fp:
            content = fp.read()
            self.content = self.loadFromString(content)
            fp.close()    
    
    def loadFromString(self, payload):
        matched = self.link_finder_re.match(payload)
        if matched:
            return matched.groups(1)[0]
        return None
    
    def _find_search_items(self):
        results = []
        if self.content != None:
            results.append(self.content)
        return results

    def _extract_dict_from_item(self, item):
        url = item
        url_p = urllib.parse.urlparse(url)
        id_annonce = url_p.path.split('/')[-1].replace(".htm", '')  
        mystruct = MESSAGE_STRUCT.copy()
        myvalues = {
        'date_mail' : datetime.fromtimestamp(self.date).strftime('%d/%m/%Y') if self.date is not None else None,
        'created_at' : datetime.fromtimestamp(self.date).strftime('%d/%m/%Y') if self.date is not None else None,
        'url' : url,
        'id_annonce': id_annonce, 
        'prix' : 0
        }
        mystruct.update(myvalues)
        return mystruct
    
    def extract_items(self):
        extract = []
        items = self._find_search_items()
        for item in items:
            extract.append(self._extract_dict_from_item(item))
        return extract
    