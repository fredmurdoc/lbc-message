import os
import os.path
from posixpath import dirname
import json
from datetime import datetime
from lbc_message import LbcMessage
from lbc_message_from_app import LbcMessageFromApp

"""
charge les fichiers du jour
force :  force le chargement de tous les fichiers et pas ceux que du jour
"""
def extract_items_from_alerts(force=False):
    url_annonces = {}
    json_content = []
    today_str = datetime.now().strftime('%Y-%m-%d')
    directory = '%s/results' % dirname(__file__)
    for payload_file in os.listdir(directory):
        f = os.path.join(directory, payload_file)
        
        extension = os.path.splitext(payload_file)[1]
        # checking if it is a file
        if os.path.isfile(f) and extension == '.html':
            file_modified_today =datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d') == today_str
            # si force pas setté et que la date de modif du fichier ne correspond pas à aujourdhui on passe
            if force == False and file_modified_today == False:
                continue
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
        value = { 'date': item['date_mail'], 'index': index, 
                 'payload_file': item['payload_file']}
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

def extract_items_from_app(force=False):
    url_annonces = {}
    json_content = []
    today_str = datetime.now().strftime('%Y-%m-%d')
    directory = '%s/results_from_app' % dirname(__file__)
    for payload_file in os.listdir(directory):
        f = os.path.join(directory, payload_file)
        extension = os.path.splitext(payload_file)[1]
        # checking if it is a file
        if os.path.isfile(f) and extension == '.html':
            file_modified_today =datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d') == today_str
        # si force pas setté et que la date de modif du fichier ne correspond pas à aujourdhui on passe
            if force == False and file_modified_today == False:
                continue
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
    items_collected = []
    # chargement des annonces du fichier précedent
    with open('items.json', 'r') as fp:
        items = json.load(fp)
        fp.close()
    # generation de la liste des ids deja chargées
    ids_annonces = [i['id_annonce'] for i in items]
    # recupération des items du jour
    items_collected = extract_items_from_alerts()
    items_collected.extend(extract_items_from_app())
    print("%s nouvelles annonces téléchargées" % len(items_collected))
    counter_new = 0
    # on regarde si l'item du jour est d"ja présente
    for item in items_collected:
        if item['id_annonce'] not in ids_annonces:
            counter_new = counter_new +1
            items.append(item)
    print("%s nouvelles annonces intégrées dans le fichier" % counter_new)

    with open('items.json', 'w') as fp:
        json.dump(items, fp)
        fp.close()