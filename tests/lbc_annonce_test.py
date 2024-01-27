from datetime import datetime
import unittest

from lbc_annonce import LbcAnnonce
import logging
import sys
import json
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
items = None

with open('items.json', 'r') as fp:
    items = json.load(fp)

class TestLbcAnnonce(unittest.TestCase):
    ok_datas = {"1":{"file":"tests/2013210401.htm","id":'2013210401',
"criteres":{'a_terrain' : True,  'surface' :  60, 'nb_pieces' :  2 , 'type_maison' : 'maison', 'surface_terrain' : 377},
"metadatas":{'code_postal': None, 'commune': None, 'date_annonce' : '23/02/2022 10:04', 'prix': 42400}
},
"2":{"file":"tests/2058131180.htm",'id':'2058131180',
     "criteres":{'a_terrain' : False,  'surface' :  156, 'nb_pieces' :  8 , 'type_maison' : 'maison', 'surface_terrain' : None},
     "metadatas":{'code_postal': None, 'commune': None,'date_annonce' : '02/02/2022 09:04', 'prix': 65000}},
"3":{"file": "tests/2418312808.htm","id":'2418312808',
     "criteres":{'a_terrain' : True,  'surface' :  76, 'nb_pieces' :  6 , 'type_maison' : 'maison', 'surface_terrain' : 1176}, 
     "metadatas":{'code_postal': '49420','commune': "Ombrée d'Anjou ",'date_annonce': None,'prix': 46000}},
"4":{"file": 'tests/2448985471_annonce_venant_partage.htm', "id":"2448985471",
     "criteres":None, 
     "metadatas":{'date_annonce' :None, 'code_postal': '49520', 'commune': 'Segré-en-Anjou Bleu ', 'date_annonce': None, 'prix': 75000}},
"5":{"file": 'tests/2363782143.htm',"id":"2363782143",
     "criteres":None, 
     "metadatas":{'date_annonce' :None, 'code_postal': '49120', 'commune': 'Chemillé-en-Anjou ', 'date_annonce': None, 'prix': 38500}},
"6":{"file": 'tests/2450313985.htm',"id":'2450313985',
     "criteres":{'a_terrain' : True,  'surface' :  60, 'nb_pieces' :  2 , 'type_maison' : 'maison', 'surface_terrain' : 578}, 
     "metadatas":{'date_annonce' :None, 'code_postal': '56910', 'commune': 'Carentoir ', 'date_annonce': None, 'prix': 52400}}
    }
    
    bad_file = 'tests/2008301422.htm'
    nonexistent = 'tests/OLKJLKJL.htm'
    empty = 'tests/empty.htm'




    def test_constructor_ok(self):
        annonce = LbcAnnonce(self.ok_datas["1"]["file"])
        self.assertIsNotNone(annonce)
        del(annonce)

    def test_constructor_ok1(self):
        annonce = LbcAnnonce(self.bad_file)
        self.assertIsNotNone(annonce)
        del(annonce)

    def test_constructor_ok4(self):
        annonce = LbcAnnonce(self.ok_datas["4"]["file"])
        self.assertIsNotNone(annonce)
        del(annonce)


    def test_constructor_emptyfile_ko(self):
        self.assertRaises(Exception, LbcAnnonce, self.empty)
        

    def test_constructor_ko(self):
        self.assertRaises(Exception, LbcAnnonce, self.nonexistent)

    def test_get_criteres_ok(self):
        annonce = LbcAnnonce(self.ok_datas["1"]["file"])
        criteres = annonce.extract_criteres()
        self.assertIsNotNone(criteres)
        self.assertEquals(criteres, self.ok_datas["1"]["criteres"])
        del(annonce)

    def test_get_criteres_ok2(self):
        annonce = LbcAnnonce(self.ok_datas["2"]["file"])
        criteres = annonce.extract_criteres()
        self.assertIsNotNone(criteres)
        self.assertEquals(criteres, self.ok_datas["2"]["criteres"])
        del(annonce)

    def test_get_criteres_ok3(self):
        annonce = LbcAnnonce(self.ok_datas["3"]["file"])
        criteres = annonce.extract_criteres()
        self.assertIsNotNone(criteres)
        self.assertEquals(criteres, self.ok_datas["3"]["criteres"])
        del(annonce)

    def test_get_criteres_ok6(self):
        annonce = LbcAnnonce(self.ok_datas["6"]["file"])
        criteres = annonce.extract_criteres()
        self.assertIsNotNone(criteres)
        self.assertEquals(criteres, self.ok_datas["6"]["criteres"])
        del(annonce)


    def test_get_extract_metadatas_ok(self):
        annonce = LbcAnnonce(self.ok_datas["1"]["file"])
        metadatas = annonce.extract_metadatas()
        self.assertIsNotNone(metadatas)
        self.assertIsNotNone(metadatas['description'])
        del(metadatas['description'])
        self.assertEquals(metadatas, self.ok_datas["1"]["metadatas"])
        del(annonce)

    def test_get_extract_metadatas_ok2(self):
        annonce = LbcAnnonce(self.ok_datas["2"]["file"])
        metadatas = annonce.extract_metadatas()
        self.assertIsNotNone(metadatas)
        self.assertIsNotNone(metadatas['description'])
        del(metadatas['description'])
        self.assertEquals(metadatas, self.ok_datas["2"]["metadatas"])
        del(annonce)

    def test_get_extract_metadatas_ok3(self):
        annonce = LbcAnnonce(self.ok_datas["3"]["file"])
        metadatas = annonce.extract_metadatas()
        self.assertIsNotNone(metadatas)
        self.assertIsNotNone(metadatas['description'])
        del(metadatas['description'])
        self.assertEquals(metadatas, self.ok_datas["3"]["metadatas"])
        del(annonce)

    def test_get_extract_metadatas_ok4(self):
        annonce = LbcAnnonce(self.ok_datas["4"]["file"])
        metadatas = annonce.extract_metadatas()
        self.assertIsNotNone(metadatas)
        print(metadatas['description'])
        self.assertIsNotNone(metadatas['description'])
        del(metadatas['description'])
        self.assertEquals(metadatas, self.ok_datas["4"]["metadatas"])
        del(annonce)

    def test_get_extract_metadatas_ok5(self):
        annonce = LbcAnnonce(self.ok_datas["5"]["file"])
        metadatas = annonce.extract_metadatas()
        self.assertIsNotNone(metadatas)
        self.assertIsNotNone(metadatas['description'])
        del(metadatas['description'])
        self.assertEquals(metadatas, self.ok_datas["5"]["metadatas"])
        del(annonce)

    def test_get_extract_image_ok5(self):
        annonce = LbcAnnonce(self.ok_datas["5"]["file"])
        img_url = annonce.extract_image()
        print(img_url)
        self.assertIsNotNone(img_url)
        del(annonce)

    
    def test_get_extract_metadatas_ok6(self):
        annonce = LbcAnnonce(self.ok_datas["6"]["file"])
        metadatas = annonce.extract_metadatas()
        self.assertIsNotNone(metadatas)
        self.assertIsNotNone(metadatas['description'])
        del(metadatas['description'])
        self.assertEquals(metadatas, self.ok_datas["6"]["metadatas"])
        del(annonce)

    
    
    
    def test_get_extract_image_desactive_ok(self):
        annonce = LbcAnnonce(self.bad_file)
        img_url = annonce.extract_image()
        print(img_url)
        self.assertIsNone(img_url)
        del(annonce)


    def test_get_extract_metadatas_ko(self):
        annonce = LbcAnnonce(self.bad_file)
        metadatas = annonce.extract_metadatas()
        self.assertIsNotNone(metadatas)
        
        del(metadatas['description'])
        self.assertEquals(metadatas, {'date_annonce' : None, 'prix': None, 'commune': None, 'code_postal': None})
        del(annonce)

    def test_get_criteres_ko(self):
        annonce = LbcAnnonce(self.bad_file)
        criteres = annonce.extract_criteres()
        self.assertIsNone(criteres)       

    def test_est_desactivee_ok(self):
        annonce = LbcAnnonce(self.bad_file)
        est_desactivee = annonce.est_desactivee()
        self.assertTrue(est_desactivee)

    def test_est_desactivee_ko(self):
        annonce = LbcAnnonce(self.ok_datas["1"]["file"])
        est_desactivee = annonce.est_desactivee()
        self.assertFalse(est_desactivee)

    def test_item_6(self):        
        annonce = LbcAnnonce(self.ok_datas["6"]["file"])
        metadatas = annonce.extract_metadatas()
        self.assertIsNotNone(metadatas)
        item = [i for i in items if i['id_annonce'] == self.ok_datas["6"]["id"]][0]
        del(metadatas['description'])
        attributes = self.ok_datas["6"]["metadatas"]
        attributes.update(self.ok_datas["6"]["criteres"])
        exceptions = ['date_annonce']
        expected = {k: attributes[k]for k in attributes.keys() if k not in exceptions}
        tested = {k: item[k]for k in attributes.keys() if k not in exceptions}
        self.assertEquals(expected, tested)
        del(annonce)

    def test_item_3(self):        
        annonce = LbcAnnonce(self.ok_datas["3"]["file"])
        metadatas = annonce.extract_metadatas()
        self.assertIsNotNone(metadatas)
        item = [i for i in items if i['id_annonce'] == self.ok_datas["3"]["id"]][0]
        del(metadatas['description'])
        attributes = self.ok_datas["3"]["metadatas"]
        attributes.update(self.ok_datas["3"]["criteres"])
        exceptions = ['date_annonce']
        expected = {k: attributes[k]for k in attributes.keys() if k not in exceptions}
        tested = {k: item[k]for k in attributes.keys() if k not in exceptions}
        self.assertEquals(expected, tested)
        del(annonce)



if __name__ == '__main__':
    unittest.main()

