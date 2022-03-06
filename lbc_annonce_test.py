from datetime import datetime
import unittest

from lbc_annonce import LbcAnnonce
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class TestLbcAnnonce(unittest.TestCase):
    good_file = 'tests/2013210401.htm'
    bad_file = 'tests/2008301422.htm'
    good_file2 = 'tests/2058131180.htm'
    nonexistent = 'tests/OLKJLKJL.htm'
    empty = 'tests/empty.htm'

    def test_constructor_ok(self):
        annonce = LbcAnnonce(self.good_file)
        self.assertIsNotNone(annonce)
        del(annonce)

    def test_constructor_ok1(self):
        annonce = LbcAnnonce(self.bad_file)
        self.assertIsNotNone(annonce)
        del(annonce)

    def test_constructor_emptyfile_ko(self):
        self.assertRaises(Exception, LbcAnnonce, self.empty)
        

    def test_constructor_ko(self):
        self.assertRaises(Exception, LbcAnnonce, self.nonexistent)

    def test_get_criteres_ok(self):
        annonce = LbcAnnonce(self.good_file)
        criteres = annonce.extract_criteres()
        self.assertIsNotNone(criteres)
        self.assertEquals(criteres, {'a_terrain' : True,  'surface' :  60, 'nb_pieces' :  2 , 'type_maison' : 'maison', 'surface_terrain' : 377})
        del(annonce)

    def test_get_criteres_ok2(self):
        annonce = LbcAnnonce(self.good_file2)
        criteres = annonce.extract_criteres()
        self.assertIsNotNone(criteres)
        self.assertEquals(criteres, {'a_terrain' : False,  'surface' :  156, 'nb_pieces' :  8 , 'type_maison' : 'maison', 'surface_terrain' : None})
        del(annonce)

    def test_get_extract_metadatas_ok(self):
        annonce = LbcAnnonce(self.good_file)
        metadatas = annonce.extract_metadatas()
        self.assertIsNotNone(metadatas)
        self.assertEquals(metadatas, {'date_annonce' : datetime.strptime('23/02/2022 10:04', '%d/%m/%Y %H:%M')})
        del(annonce)

    def test_get_extract_metadatas_ok2(self):
        annonce = LbcAnnonce(self.good_file2)
        metadatas = annonce.extract_metadatas()
        self.assertIsNotNone(metadatas)
        self.assertEquals(metadatas, {'date_annonce' : datetime.strptime('02/02/2022 09:04', '%d/%m/%Y %H:%M')})
        del(annonce)

    def test_get_extract_metadatas_ko(self):
        annonce = LbcAnnonce(self.bad_file)
        metadatas = annonce.extract_metadatas()
        self.assertIsNotNone(metadatas)
        self.assertEquals(metadatas, {'date_annonce' : None})
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
        annonce = LbcAnnonce(self.good_file)
        est_desactivee = annonce.est_desactivee()
        self.assertFalse(est_desactivee)


if __name__ == '__main__':
    unittest.main()

