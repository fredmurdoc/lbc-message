import os
from posixpath import dirname
import json
from datetime import datetime
from lbc_annonce import LbcAnnonce
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
def extract_annonces():
    items = []
    items_file = 'items.json'
    url_annonces = {}
    json_content = []
    is_updated_at = datetime.now().strftime('%Y-%m-%d')
    directory = 'annonces'
    for annonce_file in os.listdir(directory):
        
        html_file_annonce_path = os.path.join(directory, annonce_file)
        logging.info("parse file %s" % html_file_annonce_path)
        extension = os.path.splitext(annonce_file)[1]
        # checking if it is a file
        if os.path.isfile(html_file_annonce_path) and extension == '.htm':
            #get payload file
            print('analyze payload file %s' % annonce_file)
            #analyse it
            lbc_annonce = LbcAnnonce(html_file=html_file_annonce_path)
            item = {}
            item['desactivee'] =  lbc_annonce.est_desactivee()
            
            logging.debug("item['desactivee'] %s " % item['desactivee'])
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
            items.append(item)

        

    with open(items_file, 'w') as fp:
        json.dump(items, fp)
            
if __name__ == '__main__':
    extract_annonces()