import json
import os
import sys
import urllib3
items_fp =open('items.json', 'r')
items = json.load(items_fp)
nb_to_open=20
counter = 0
urls_to_open = []


lbc_part_to_delete = '/vi/'


for item in items:
    
    url = urllib3.util.parse_url(item['url'])
    html_file_annonce = url.path.replace(lbc_part_to_delete, '').replace('/', '')
    html_file_annonce_path ='annonces/%s' % html_file_annonce
    if os.path.exists(html_file_annonce_path):
        print('file %s exists pass' % html_file_annonce_path)
        continue
    counter += 1
    if counter <= nb_to_open:
        urls_to_open.append(item['url'])
    else:
        print("collected %d urls stop" % len(urls_to_open))
        break

os.system('firefox %s' % " ".join(urls_to_open))