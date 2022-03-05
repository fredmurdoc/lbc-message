import json
import logging
import os
import sys
import urllib3
from lbc_annonce import LbcAnnonce
from bs4 import BeautifulSoup

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

items_file = 'items.json'
items_fp =open(items_file, 'r')

items = json.load(items_fp)

lbc_part_to_delete = '/vi/'


for key_item, item in enumerate(items):
    
    url = urllib3.util.parse_url(item['url'])
    html_file_annonce = url.path.replace(lbc_part_to_delete, '').replace('/', '')
    html_file_annonce_path ='annonces/%s' % html_file_annonce
    if os.path.exists(html_file_annonce_path):
        print('analyse annonce %s' % html_file_annonce_path)
        annonce = LbcAnnonce(html_file_annonce_path)
        item['desactivee'] =  annonce.est_desactivee()
        logging.debug("item['desactivee'] %s " % item['desactivee'])
        if item['desactivee'] == False:
            criteres = annonce.extract_criteres()
            if criteres is not None:
                logging.debug('criteres')
                logging.debug(criteres)
                for k in criteres.keys():
                    if k in item and item[k] is None:
                        item[k] = criteres[k] 
            else:
                logging.debug(criteres)
                logging.error('annonce %s est active mais pas de criteres', html_file_annonce_path)
        items[key_item] = item    
    else:
        continue

with open(items_file, 'w') as fp:
    json.dump(items, fp)