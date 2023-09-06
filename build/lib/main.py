from sqlite3 import Date
from gmail import Gmail, GmailFilter
from lbc_message import LbcMessage
from posixpath import dirname
from datetime import datetime, timedelta

def main():
    cred_file = "%s/credentials.json" % dirname(__file__)
    token_file = "%s/token.json" % dirname(__file__)
    print("load files %s and %s " % (cred_file, token_file))
    gmail = Gmail(credentials_file=cred_file, token_file=token_file)
    
    originDate = datetime.strptime('01/01/2015', '%d/%m/%Y')
    originDate = datetime.now() - timedelta(weeks=4)
    print("date de recherche de départ %s" % originDate.strftime('%d/%m/%Y'))
    subjects = ['Maison', 'Ventes immobilières', 'eVentes immobilières', 'Chateaubriand', 'maison', 'maisons']
    messages = None
    for subject in subjects:
        filter = GmailFilter()
        filter.fromEmail('leboncoin').subject(subject).fromDate(originDate)
        if messages is None:
            messages = gmail.listMessages(filter)
        else:
            messages.extend(gmail.listMessages(filter))        
    
    print("retrieve %d messages " % len(messages))
    json_content = []
    for msg in messages:
        real_message = gmail.getMessage(msg['id'])
        date_received = datetime.fromtimestamp(float(real_message['internalDate'])/1000)
        print("msg id [%s], recu [%s] : %s" % (msg['id'], date_received, real_message['snippet']))
        try:
            gmail.saveMessageToFolder(folder = '%s/results' % dirname(__file__), msg = real_message, overwrite=False)
            print("OK !!!!!! message %s saved" % msg['id'])
        except FileExistsError as e:
            print('already exists')
        except Exception as ee:
            print("message file error")
            print(ee)
        
        try:
            gmail.saveMessagePayloadToFolder(folder = '%s/results' % dirname(__file__), msg = real_message, overwrite=False)
            print("OK !!!!!!! message %s payload saved" % msg['id'])
        except FileExistsError as e:
            print("already exists")
        except Exception as ee:
            print("payload file error")
            print(ee)


if __name__ == '__main__':
    main()