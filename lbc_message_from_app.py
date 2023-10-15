from termios import VT1
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import etree
import re
import logging
import os.path
from enum import Enum
        
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
        return {
        'date_mail' : datetime.fromtimestamp(self.date).strftime('%Y-%m-%d') if self.date is not None else None,
        'created_at' : datetime.fromtimestamp(self.date).strftime('%Y-%m-%d') if self.date is not None else None,
        'url' : item,
        'prix' : 0,
        'intitule' : "",
        'commune' : "",
        'code_postal' : "",
        'image_url' : "",
        'superficie' : "",
        'nb_pieces' : ""
        }
    
    def extract_items(self):
        extract = []
        items = self._find_search_items()
        for item in items:
            extract.append(self._extract_dict_from_item(item))
        return extract
    