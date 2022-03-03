from posixpath import dirname
from gmail import Gmail, GmailFilter
import json
from datetime import datetime
from lbc_message import LbcMessage

overWrite = False

def main():
    gmail = Gmail(credentials_file="%s/credentials.json" % dirname(__file__), token_file="%s/token.json" % dirname(__file__))
    filter = GmailFilter()
    originDate = datetime.strptime('01/01/2015', '%d/%m/%Y')
    filter.fromEmail('leboncoin').subject("Maison").fromDate(originDate)
    
    messages = gmail.listMessages(filter)
    
    filter = GmailFilter()
    filter.fromEmail('leboncoin').subject("Ventes immobilières").fromDate(originDate)
    messages.extend(gmail.listMessages(filter))

    filter = GmailFilter()
    filter.fromEmail('leboncoin').subject("eVentes immobilières")
    messages.extend(gmail.listMessages(filter))

    print("retrieve %d messages " % len(messages))
    json_content = []
    for msg in messages:
        print("msg %s" % msg['id'])
        real_message = gmail.getMessage(msg['id'])
        try:
            gmail.saveMessageToFolder(folder = '%s/results' % dirname(__file__), msg = real_message, overwrite=overWrite)
            print("message %s saved" % msg['id'])
        except FileExistsError as e:
            print("message file error")
            print(e)
        except Exception as ee:
            print("message file error")
            print(ee)
        
        try:
            gmail.saveMessagePayloadToFolder(folder = '%s/results' % dirname(__file__), msg = real_message, overwrite=overWrite)
            print("message %s payload saved" % msg['id'])
        except FileExistsError as e:
            print("payload file error")
            print(e)
        except Exception as ee:
            print("payload file error")
            print(ee)

        #get payload file
        payload_file = gmail.getPayloadPath(folder='%s/results' % dirname(__file__), msg = real_message)
        print('analyze payload file %s' % payload_file)
        #analyse it
        lbc_msg = LbcMessage()
        lbc_msg.loadFromFile(payload_file)
        try:
            extracted = lbc_msg.extract_items()
            json_content.extend(extracted)
        except Exception as e:
            print(e)    
        
    with open('items.json', 'w') as fp:
        json.dump(json_content, fp)
        fp.close()
if __name__ == '__main__':
    main()