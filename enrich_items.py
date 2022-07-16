import json
import logging
import os
import sys
import urllib3
from datetime import datetime
from lbc_annonce import LbcAnnonce
from bs4 import BeautifulSoup
import time
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

items_file = 'items.json'
items_fp =open(items_file, 'r')

items = json.load(items_fp)

lbc_part_to_delete = '/vi/'

is_updated_at = datetime.now().strftime('%Y-%m-%d')

for key_item, item in enumerate(items):
    
    url = urllib3.util.parse_url(item['url'])
    html_file_annonce = url.path.replace(lbc_part_to_delete, '').replace('/', '')
    html_file_annonce_path ='annonces/%s' % html_file_annonce
    if os.path.exists(html_file_annonce_path):
        print('analyse annonce %s' % html_file_annonce_path)
        annonce = LbcAnnonce(html_file_annonce_path)
        item['desactivee'] =  annonce.est_desactivee()
        item['id_annonce'] = annonce.extract_id()
        logging.debug("item['desactivee'] %s " % item['desactivee'])
        if item['desactivee'] == False:
            criteres = annonce.extract_criteres()
            if criteres is not None:
                logging.debug('criteres')
                logging.debug(criteres)
                for k in criteres.keys():
                    if criteres[k] is not None:
                        item[k] = criteres[k] 
            else:
                logging.debug(criteres)
                logging.error('annonce %s est active mais pas de criteres', html_file_annonce_path)
            
            metadatas = annonce.extract_metadatas()
            if metadatas is not None:
                logging.debug('metadatas')
                logging.debug(metadatas)
                for k in metadatas.keys():
                    if metadatas[k] is not None:
                        item[k] = metadatas[k] 
            else:
                logging.debug(metadatas)
                logging.error('annonce %s est active mais pas de metadatas', html_file_annonce_path)
        else:
            if 'date_desactivation' not in item:
                item['date_desactivation'] = is_updated_at
        # on fixe la date de maj à la date de mise à jour du fichier HTML
        time_html= os.path.getmtime(html_file_annonce_path)
        convert_time = time.localtime(time_html)
        date_fichier = time.strftime('%Y-%m-%d', convert_time)
        item['updated_at'] = max(date_fichier, item['created_at'], item['date_mail'])
        print('annonce %s date maj %s ' % (item['id_annonce'], item['updated_at']))
                        
        #update collections
        items[key_item] = item  
    else:
        continue    

with open(items_file, 'w') as fp:
    json.dump(items, fp)