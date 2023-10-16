import json
import os
import sys
import urllib3
items_fp =open('items.json', 'r')
items = json.load(items_fp)
nb_to_open=50
counter = 0
urls_to_open = []


lbc_part_to_delete = '/vi/'


for item in items:
    html_file_annonce_path ='annonces/%s.htm' % item['id_annonce']
    if os.path.exists(html_file_annonce_path):
        #print('file %s exists pass' % html_file_annonce_path)
        continue
    counter += 1
    if counter <= nb_to_open:
        print('fichier mail recu à ouvrir : %s' % item['payload_file'])
        urls_to_open.append(item['url'])
    else:
        print("collected %d urls stop" % len(urls_to_open))
        break

os.system('firefox %s' % " ".join(urls_to_open))