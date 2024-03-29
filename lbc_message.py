from termios import VT1
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import etree
import re
import logging
import os.path
import urllib.parse
from enum import Enum

class LbcMessageXpathFinderV1():
    ITEMS_PARENT_TAG_TR = '//td/a[contains(@href, "[MYSRCH]") and span]/../..'
    ITEM_IMAGE_STYLE = './td[1]/div'
    ITEM_URL = './td[2]/a'
    ITEM_INTITULE = './td[2]/a/span[1]'
    ITEM_PRIX = './td[2]/a/span[2]'
    ITEM_COMMUNE = './td[2]/a/div/span[1]'

class LbcMessageXpathFinderV2():
    ITEMS_PARENT_TAG_TR = '//td[a and table]/a[contains(@href, "[MYSRCH]")]/../..'
    ITEM_IMAGE_STYLE = './td[1]/div'
    ITEM_URL = './td/a[contains(@href, "[MYSRCH]") and span]'
    ITEM_INTITULE = './td[2]/a/span[1]'
    ITEM_PRIX = './td[2]/a/span[2]'
    ITEM_COMMUNE = './td[2]/a/div/span[1]'

MESSAGE_STRUCT = {
        'date_mail' : None,
        'created_at' : None,
        'url' : None,
        'id_annonce' : None,
        'prix' : None,
        'intitule' : None,
        'commune' : None,
        'code_postal' : None,
        'image_url' : None,
        'superficie' : None,
        'nb_pieces' : None
        }

class LbcMessage:
    REGEXP_SUPERFICIE = r'.+\s+(?P<superficie>[0-9]+)\s+m\u00b2.*'
    REGEXP_NBPIECES= r'.+\s+(?P<nb_pieces>[0-9]+)\s+pièce.\s+.*'
    REGEXP_COMMUNE_CP= r'\s*(?P<commune>[^0-9]+)\s+(?P<cp>[0-9]{5})\s*'
    def __init__(self):
        self.finder = None
        self.date = None
    def loadFromFile(self, file):
        self.date = os.path.getmtime(file)
        with open(file, 'r') as fp:
            content = fp.read()
            self.loadFromString(content)
            fp.close()    
    
    def loadFromString(self, payload):
        soup = BeautifulSoup(payload, "html.parser")
        self.dom = etree.HTML(str(soup))
        logging.debug(etree.tostring(self.dom))
    
    def _find_search_items(self):
        results = self.dom.xpath(LbcMessageXpathFinderV1.ITEMS_PARENT_TAG_TR)
        self.finder = LbcMessageXpathFinderV1
        if results is None or len(results) == 0:
            results = self.dom.xpath(LbcMessageXpathFinderV2.ITEMS_PARENT_TAG_TR)
            self.finder = LbcMessageXpathFinderV2
        if results is None or len(results) == 0:
            raise Exception('cannot find compatible finder')    
        return results

    def _find_search_item_url(self, parent_item):
        element = parent_item.find(self.finder.ITEM_URL)
        return element.attrib['href'] if element is not None else None

    def _find_search_item_superficie(self, parent_item):
        description = self._find_search_ITEM_INTITULE(parent_item)
        if description is None:
            return None
        m = re.search(self.REGEXP_SUPERFICIE, description)
        return int(m.group('superficie')) if m is not None else None

    def _find_search_item_nb_pieces(self, parent_item):
        description = self._find_search_ITEM_INTITULE(parent_item)
        if description is None:
            return None
        m = re.search(self.REGEXP_NBPIECES, description)
        return int(m.group('nb_pieces')) if m is not None else None


    def _find_search_ITEM_INTITULE(self, parent_item):
        element = parent_item.find(self.finder.ITEM_INTITULE)
        return element.text if element is not None else None

    def _find_search_item_prix(self, parent_item):
        element = parent_item.find(self.finder.ITEM_PRIX)
        return int(element.text.split(' ')[0]) if element is not None else None

    def _find_search_item_commune_cp(self, parent_item):
        element = parent_item.find(self.finder.ITEM_COMMUNE)
        return element.text if element is not None else None

    def _find_search_item_commune(self, parent_item):
        com_cp = self._find_search_item_commune_cp(parent_item)
        if com_cp is None:
            return None
        m = re.search(self.REGEXP_COMMUNE_CP, com_cp)
        return m.group('commune') if m is not None else None

    def _find_search_item_commune_codepostal(self, parent_item):
        com_cp = self._find_search_item_commune_cp(parent_item)
        if com_cp is None:
            return None
        m = re.search(self.REGEXP_COMMUNE_CP, com_cp)
        return m.group('cp') if m is not None else None


    def _find_search_item_image_url(self, parent_item):
        element =  parent_item.find(self.finder.ITEM_IMAGE_STYLE)
        style_string = element.attrib['style']
        for style_attr_raw in style_string.split(';'):
            style_attr = style_attr_raw.strip()
            if 'background-image:' in style_attr:
                value = style_attr[len('background-image:'):]
                if value is None:
                    return value
                reg_val =re.search('url\((.+)\)', value.strip())
                if reg_val is None:
                    return None
                return reg_val.group(1)    

        
    def _extract_dict_from_parent_item(self, parent_item):
        url = self._find_search_item_url(parent_item)
        url_p = urllib.parse.urlparse(url)
        if url_p.path.endswith('/'):
            id_annonce = url_p.path.split('/')[-2].replace(".htm", '')  
        else:
            id_annonce = url_p.path.split('/')[-1].replace(".htm", '')  
        mystruct = MESSAGE_STRUCT.copy()
        myvalues ={
        'date_mail' : datetime.fromtimestamp(self.date).strftime('%Y-%m-%d') if self.date is not None else None,
        'created_at' : datetime.fromtimestamp(self.date).strftime('%Y-%m-%d') if self.date is not None else None,
        'url' : url,
        'id_annonce' : id_annonce,
        'prix' : self._find_search_item_prix(parent_item),
        'intitule' : self._find_search_ITEM_INTITULE(parent_item),
        'commune' : self._find_search_item_commune(parent_item),
        'code_postal' : self._find_search_item_commune_codepostal(parent_item),
        'image_url' : self._find_search_item_image_url(parent_item),
        'superficie' : self._find_search_item_superficie(parent_item),
        'nb_pieces' : self._find_search_item_nb_pieces(parent_item)
        }
        mystruct.update(myvalues)
        return mystruct
    
    def extract_items(self):
        extract = []
        items = self._find_search_items()
        for item in items:
            extract.append(self._extract_dict_from_parent_item(item))
        return extract
    