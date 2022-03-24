from gmail import Gmail, GmailFilter
from lbc_message import LbcMessage
from posixpath import dirname
from datetime import datetime

def main():
    cred_file = "%s/credentials.json" % dirname(__file__)
    token_file = "%s/token.json" % dirname(__file__)
    print("load files %s and %s " % (cred_file, token_file))
    gmail = Gmail(credentials_file=cred_file, token_file=token_file)
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


    filter = GmailFilter()
    filter.fromEmail('leboncoin').subject("Chateaubriand")
    messages.extend(gmail.listMessages(filter))

    filter = GmailFilter()
    filter.fromEmail('leboncoin').subject("maison")
    messages.extend(gmail.listMessages(filter))


    print("retrieve %d messages " % len(messages))
    json_content = []
    for msg in messages:
        print("msg %s" % msg['id'])
        real_message = gmail.getMessage(msg['id'])
        try:
            gmail.saveMessageToFolder(folder = '%s/results' % dirname(__file__), msg = real_message, overwrite=False)
            print("message %s saved" % msg['id'])
        except FileExistsError as e:
            print("message file error")
            print(e)
        except Exception as ee:
            print("message file error")
            print(ee)
        
        try:
            gmail.saveMessagePayloadToFolder(folder = '%s/results' % dirname(__file__), msg = real_message, overwrite=False)
            print("message %s payload saved" % msg['id'])
        except FileExistsError as e:
            print("payload file error")
            print(e)
        except Exception as ee:
            print("payload file error")
            print(ee)


if __name__ == '__main__':
    main()