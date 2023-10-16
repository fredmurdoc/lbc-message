import json
import os
import sys
import urllib3
items_fp =open('items.json', 'r')
items = json.load(items_fp)
nb_to_open=40
results = {'downloaded':0, 'not_downloaded':0}

lbc_part_to_delete = '/vi/'


for item in items:
    
    html_file_annonce_path ='annonces/%s.htm' % item['id_annonce']
    if os.path.exists(html_file_annonce_path):
        results['downloaded'] +=1
    else:
        results['not_downloaded'] +=1


print(results)