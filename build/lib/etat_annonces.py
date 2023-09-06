import json
import os
import sys
import urllib3
items_fp =open('items.json', 'r')
items = json.load(items_fp)
nb_to_open=40
results = {'downloaded':0, 'not_downloaded':0}
urls_to_open = []


lbc_part_to_delete = '/vi/'


for item in items:
    
    url = urllib3.util.parse_url(item['url'])
    html_file_annonce = url.path.replace(lbc_part_to_delete, '').replace('/', '')
    html_file_annonce_path ='annonces/%s' % html_file_annonce
    if os.path.exists(html_file_annonce_path):
        results['downloaded'] +=1
    else:
        results['not_downloaded'] +=1


print(results)