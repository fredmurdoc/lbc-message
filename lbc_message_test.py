import unittest
from lbc_message import LbcMessage, LbcMessageXpathFinderV1, LbcMessageXpathFinderV2
from lxml import etree
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
class TestLbcMessage(unittest.TestCase):

    def test_init_v1_ok(self):
        lbc_msg = LbcMessage()
        lbc_msg.loadFromFile('tests/v1.html')
        self.assertIsNotNone(lbc_msg.dom)

    def test_init_v2_ok(self):
        lbc_msg = LbcMessage()
        lbc_msg.loadFromFile('tests/v2.html')
        self.assertIsNotNone(lbc_msg.dom)

    def test_init_v2a_ko(self):
        lbc_msg = LbcMessage()
        try:
            lbc_msg.loadFromFile('tests/v2a.html')
            self.assertFalse(True)
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_find_search_items_v1(self):
        lbc_msg = LbcMessage()
        lbc_msg.loadFromFile('tests/v1.html')
        items = lbc_msg._find_search_items()
        self.assertIsNotNone(items)
        self.assertGreater(len(items), 0)

    def test_find_search_items_and_guess_finder_v1(self):
        lbc_msg = LbcMessage()
        lbc_msg.loadFromFile('tests/v1.html')
        lbc_msg._find_search_items()
        self.assertEqual(LbcMessageXpathFinderV1, lbc_msg.finder)


    def test_find_search_items_v2(self):
        lbc_msg = LbcMessage()
        lbc_msg.loadFromFile('tests/v2.html')
        items = lbc_msg._find_search_items()
        self.assertIsNotNone(items)
        self.assertGreater(len(items), 0)

    def test_find_search_items_and_guess_finder_v2(self):
        lbc_msg = LbcMessage()
        lbc_msg.loadFromFile('tests/v2.html')
        lbc_msg._find_search_items()
        self.assertEqual(LbcMessageXpathFinderV1, lbc_msg.finder)


    def get_first_item(self, fileTested):
        self.lbc_msg = LbcMessage()
        self.lbc_msg.loadFromFile(fileTested)
        items = self.lbc_msg._find_search_items()
        logging.debug('##############')
        logging.debug(items[0].tag)
        logging.debug(etree.tostring(items[0]))
        return items[0]

    def debug_element(self, elem):
        logging.debug("### CHILD of %s" % elem.tag)
        for child in elem.iter():
            logging.debug('-----')
            logging.debug(child.tag)
            logging.debug(etree.tostring(child))
    def assert_url(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.lbc_msg._find_search_item_url(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)
        

    def assert_image(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.lbc_msg._find_search_item_image_url(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)
    
    def assert_description(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.lbc_msg._find_search_item_description(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)
    
    def assert_superficie(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.lbc_msg._find_search_item_superficie(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)
    
    def assert_nbpieces(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.lbc_msg._find_search_item_nb_pieces(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)
        
    
    def assert_commune(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.lbc_msg._find_search_item_commune(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)

    def assert_commune_codepostal(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.lbc_msg._find_search_item_commune_codepostal(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)

    def assert_prix(self, fileTested, expected):
        item = self.get_first_item(fileTested)
        value = self.lbc_msg._find_search_item_prix(item)
        self.assertIsNotNone(value)
        self.assertEquals(expected, value)

    def test_find_search_item_url_v1(self):
        self.assert_url('tests/v1.html', 'https://www.leboncoin.fr/vi/2000407154.htm/#xtor=ES-3999-[MYSRCH]')

    def test_find_search_item_image_url_v1(self):
        self.assert_image('tests/v1.html', 'https://img.leboncoin.fr/api/v1/lbcpb1/images/93/6c/48/936c485fec35759f7901d90e5e0276c0fef37ec5.jpg?rule=ad-small')

    def test_find_search_item_description_v1(self):
        self.assert_description('tests/v1.html', 'Maison 1 pièce 60 m²')
    
    def test_find_search_item_superficie_v1(self):
        self.assert_superficie('tests/v1.html', '60')

    def test_find_search_item_superficie_v1(self):
        self.assert_nbpieces('tests/v1.html', '1')
    
    def test_find_search_item_prix_v1(self):
        self.assert_prix('tests/v1.html', '58000')
        
    def test_find_search_item_commune_v1(self):
        self.assert_commune('tests/v1.html', 'Treffieux')
    
    def test_find_search_item_codepostal_v1(self):
        self.assert_commune_codepostal('tests/v1.html', '44170')
        

    def test_find_search_item_url_v2(self):
        self.assert_url('tests/v2.html', 'https://www.leboncoin.fr/vi/1980574792.htm/#xtor=ES-3999-[MYSRCH]')

    def test_find_search_item_image_url_v2(self):
        item = self.get_first_item('tests/v2.html')
        self.debug_element(item)
        self.assert_image('tests/v2.html', 'https://img.leboncoin.fr/api/v1/lbcpb1/images/39/83/fc/3983fc7aefb64ec43b0b0559a9b09f8a35fcfdf7.jpg?rule=ad-small')

    def test_find_search_item_description_v2(self):
        self.assert_description('tests/v2.html', 'Longère 5 pièces 140 m²')

    def test_find_search_item_superficie_v1(self):
        self.assert_superficie('tests/v2.html', '140')

    def test_find_search_item_superficie_v1(self):
        self.assert_nbpieces('tests/v2.html', '5')

    def test_find_search_item_prix_v2(self):
        self.assert_prix('tests/v2.html', '74990')
        
    def test_find_search_item_commune_v2(self):
        self.assert_commune('tests/v2.html', 'Saint-Aubin-des-Châteaux')
    
    def test_find_search_item_codepostal_v2(self):
        self.assert_commune_codepostal('tests/v2.html', '44110')

if __name__ == '__main__':
    unittest.main()

