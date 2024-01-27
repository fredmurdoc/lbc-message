import json
import logging
import os
import sys
import urllib3
from datetime import datetime
from lbc_annonce import LbcAnnonce
from bs4 import BeautifulSoup
import time
import re
from lbc_message import MESSAGE_STRUCT

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

html_file_re = re.compile('.+\/(\d+\.htm).*')
items_file = 'items.json'
items_fp =open(items_file, 'r')

items = json.load(items_fp)

lbc_part_to_delete = '/vi/'

is_updated_at = datetime.now().strftime('%d/%m/%Y')
# on parcours le fichier items.json et on regarde les annonces correspondantes dans les repertoire annocnes
for key_item, item in enumerate(items):
    logging.debug("FROM ITEMS JSON item : %s" % item)
    matched = html_file_re.match(item['url'])
    if matched:
        html_file_annonce = matched.groups(1)[0]
    else :    
        url = urllib3.util.parse_url(item['url'])
        html_file_annonce = url.path.split('/')[-1]
    html_file_annonce_path ='annonces/%s' % html_file_annonce
    
    if os.path.exists(html_file_annonce_path):
        logging.info('FROM ITEMS JSON : analyse annonce %s' % html_file_annonce_path)
        annonce = LbcAnnonce(html_file_annonce_path)
        item['desactivee'] =  annonce.est_desactivee()
        item['id_annonce'] =  annonce.id_annonce
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
        time_html_modification= os.path.getmtime(html_file_annonce_path)
        time_html_creation= os.path.getctime(html_file_annonce_path)
        convert_time_html_creation = time.localtime(time_html_creation)
        convert_time_html_modification = time.localtime(time_html_modification)
        date_creation_fichier = time.strftime('%d/%m/%Y', convert_time_html_creation)
        date_modification_fichier = time.strftime('%d/%m/%Y', convert_time_html_modification)
        item['updated_at'] = date_modification_fichier
        item['date_annonce'] = item['date_annonce'] if 'date_annonce' in item.keys() and item['date_annonce'] is not None else date_creation_fichier
        print('annonce %s date maj %s ' % (item['id_annonce'], item['updated_at']))
        if 'image_url' not in item or item['image_url'] is None:
            item['image_url'] = annonce.extract_image()
        if 'intitule' in item and item['intitule'] is not None and 'description' in item and item['description'] is not None:
            item['intitule'] = item['description']
        #update collections
        items[key_item] = item  
    else:
        continue    

ids_annonces = [i['id_annonce'] for i in items]
# on scnanne tout ce qu'il y a dans le repertoie annonces et celles qui ne sont pas dans items.json on les crée
directory = 'annonces'

for annonce_file in os.listdir(directory):
    html_file_annonce_path = os.path.join(directory, annonce_file)
    logging.info("FROM HTML FILE: parse file %s" % html_file_annonce_path)
    id_annonce =os.path.splitext(annonce_file)[0]
    # si l'id annonce est dans items.json on passe
    if id_annonce  in  ids_annonces:
        logging.debug("FROM HTML FILE: annonce %s already present" % (id_annonce))
        continue
    
    
    extension = os.path.splitext(annonce_file)[1]
    # checking if it is a file
    if os.path.isfile(html_file_annonce_path) and extension == '.htm':
        logging.info('FROM HTML FILE: NEW ANNONCE !! %s' % id_annonce )
        #get payload file
        logging.info('FROM HTML FILE: analyze payload file %s' % annonce_file)
        time_html= os.path.getmtime(html_file_annonce_path)
        convert_time = time.localtime(time_html)
        date_fichier = time.strftime('%d/%m/%Y', convert_time)
        #analyse it
        lbc_annonce = LbcAnnonce(html_file=html_file_annonce_path)
        item = MESSAGE_STRUCT.copy()
        item['id_annonce'] = id_annonce
        item['desactivee'] =  lbc_annonce.est_desactivee()
        item['url'] = 'https://www.leboncoin.fr/ventes_immobilieres/%s.htm' % id_annonce
        item['created_at'] = date_fichier
        item['date_mail'] = date_fichier
        
        logging.info("FROM HTML FILE: item %s desactivee : %s " % (id_annonce, item['desactivee']))
        if item['desactivee'] == False:
            criteres = lbc_annonce.extract_criteres()
            if criteres is not None:
                logging.debug('criteres')
                logging.debug(criteres)
                item['updated_at'] = is_updated_at
                for k in criteres.keys():
                    if criteres[k] is not None:
                        item[k] = criteres[k] 
            else:
                logging.debug(criteres)
                logging.error('annonce %s est active mais pas de criteres', html_file_annonce_path)
            
        metadatas = lbc_annonce.extract_metadatas()
        if metadatas is not None:
            logging.debug('metadatas')
            logging.debug(metadatas)
            item['updated_at'] = is_updated_at
            for k in metadatas.keys():
                if metadatas[k] is not None:
                    item[k] = metadatas[k]
        
        else:
            logging.debug(metadatas)
            logging.error('annonce %s est active mais pas de metadatas', html_file_annonce_path)
        
        if 'image_url' not in item or item['image_url'] is None:
            item['image_url'] = lbc_annonce.extract_image()
        if 'intitule' in item and item['intitule'] is not None and 'description' in item and item['description'] is not None:
            item['intitule'] = item['description']
        item['date_annonce'] = item['date_annonce'] if 'date_annonce' in item.keys() and item['date_annonce'] is not None else date_fichier
        logging.info('append item %s' % id_annonce)
        items.append(item)


with open(items_file, 'w') as fp:
    json.dump(items, fp)