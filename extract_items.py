import os
from posixpath import dirname
import json
from datetime import datetime
from lbc_message import LbcMessage
from lbc_message_from_app import LbcMessageFromApp

def extract_items_from_alerts():
    url_annonces = {}
    json_content = []
    
    directory = '%s/results' % dirname(__file__)
    for payload_file in os.listdir(directory):
        f = os.path.join(directory, payload_file)
        extension = os.path.splitext(payload_file)[1]
        # checking if it is a file
        if os.path.isfile(f) and extension == '.html':
            #get payload file
            print('analyze payload file %s' % payload_file)
            #analyse it
            lbc_msg = LbcMessage()
            lbc_msg.loadFromFile(f)
            try:
                extracted = lbc_msg.extract_items()
                # on ajoute des metadonnées (dont le nom du fichier)
                for i, ext in enumerate(extracted):
                    ext['payload_file'] = f
                    extracted[i] = ext
                json_content.extend(extracted)
            except Exception as e:
                print(e)    
    #on recherche les annonces en doublons 
    for index, item in enumerate(json_content):
        can_append = False
        key =item['url']
        value = { 'date': item['date_mail'], 'index': index, 'payload_file': item['payload_file']}
        if item['url'] not in url_annonces.keys():
            can_append = True
        else: #si la date croisée est plus recente on la conserve comme reference et 
            if url_annonces[item['url']]['date'] < item['date_mail']:
                can_append = True
        if can_append:
            url_annonces[key] = value
    
    items = []
    # on ajoute que les items a conserver
    for url, item_to_keep in url_annonces.items():
        #print('annonce a ouvrir (%s), fichier %s ' % (item_to_keep['date'], item_to_keep['payload_file'] ))
        items.append(json_content[item_to_keep['index']])
    return items

def extract_items_from_app():
    url_annonces = {}
    json_content = []
    
    directory = '%s/results_from_app' % dirname(__file__)
    for payload_file in os.listdir(directory):
        f = os.path.join(directory, payload_file)
        extension = os.path.splitext(payload_file)[1]
        # checking if it is a file
        if os.path.isfile(f) and extension == '.html':
            #get payload file
            print('analyze payload file %s' % payload_file)
            #analyse it
            lbc_msg = LbcMessageFromApp()
            lbc_msg.loadFromFile(f)
            try:
                extracted = lbc_msg.extract_items()
                # on ajoute des metadonnées (dont le nom du fichier)
                for i, ext in enumerate(extracted):
                    ext['payload_file'] = f
                    extracted[i] = ext
                json_content.extend(extracted)
            except Exception as e:
                print(e)    
    #on recherche les annonces en doublons 
    for index, item in enumerate(json_content):
        can_append = False
        key =item['url']
        value = { 'date': item['date_mail'], 'index': index, 'payload_file': item['payload_file']}
        if item['url'] not in url_annonces.keys():
            can_append = True
        else: #si la date croisée est plus recente on la conserve comme reference et 
            if url_annonces[item['url']]['date'] < item['date_mail']:
                can_append = True
        if can_append:
            url_annonces[key] = value
    
    items = []
    # on ajoute que les items a conserver
    for url, item_to_keep in url_annonces.items():
        #print('annonce a ouvrir (%s), fichier %s ' % (item_to_keep['date'], item_to_keep['payload_file'] ))
        items.append(json_content[item_to_keep['index']])
    return items


    


if __name__ == '__main__':
    items = []
    items = extract_items_from_alerts()
    items.extend(extract_items_from_app())
    with open('items.json', 'w') as fp:
        json.dump(items, fp)
        fp.close()