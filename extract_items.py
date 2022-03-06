import os
from posixpath import dirname
import json
from datetime import datetime
from lbc_message import LbcMessage

def extract_items():
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
                json_content.extend(extracted)
            except Exception as e:
                print(e)    
        
    with open('items.json', 'w') as fp:
        json.dump(json_content, fp)
        fp.close()

if __name__ == '__main__':
    extract_items()