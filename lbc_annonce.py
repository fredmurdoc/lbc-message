from bs4 import BeautifulSoup
import logging
import sys
from datetime import datetime

class LbcAnnonce():
    fp_html = None
    def __init__(self, html_file):
        self.fp_html = open(html_file, 'r')
        self.soup = BeautifulSoup(self.fp_html, features='lxml')
        if len(self.soup) == 0:
            raise Exception("file %s is empty" % self.fp_html.name)
    
    def __del__(self):
        if self.fp_html is not None:
            self.fp_html.close()

    def est_desactivee(self):
        annonce_desactivee = self.soup.find(string='Cette annonce est désactivée')
        return annonce_desactivee is not None

    def extract_metadatas(self):
        p_data_annonce = self.soup.find('p', attrs={'data-qa-id' : "adview_date"})
        date_annonce = datetime.strptime(p_data_annonce.text, '%d/%m/%Y à %H:%M').strftime('%d/%m/%Y %H:%M') if p_data_annonce is not None else None
        p_data_prix = self.soup.find('div', attrs={'data-qa-id' : "adview_price"})
        prix_annonce = int(p_data_prix.text.replace('€', '').replace(' ', '').replace('\u202f', '').replace('\u202f', '\xa0')) if p_data_prix is not None else None
        return { 'date_annonce' : date_annonce, 'prix': prix_annonce}

    def extract_criteres(self):
        criteres = self.soup.find(string='Critères')
        if criteres is None:
            return None
        divs_criteres = criteres.find_parent('div')
        logging.debug(divs_criteres)
        spans_criteres = divs_criteres.find_all('span')
        logging.debug(spans_criteres)
        a_terrain = False
        surface, nb_pieces, type_maison, surface_terrain = [None, None, None, None]
        for span in spans_criteres:
            if 'Surface de ' in span.text:
                surface=span.text.replace('Surface de ', '').replace(' m\u00b2', '')
            if 'Maison' in span.text:
                type_maison = 'maison'
            if 'pièces' in span.text:
                nb_pieces = span.text.replace(' pièces', '').replace(' pièce', '')
            if 'Terrain de 'in span.text:
                surface_terrain=span.text.replace('Terrain de ', '').replace(' m\u00b2', '')
                a_terrain = True
        return { 'a_terrain' : a_terrain,  'surface' : int(surface) if surface is not None else None, 'nb_pieces' : int(nb_pieces) if nb_pieces is not None else None , 'type_maison' : type_maison, 'surface_terrain' : int(surface_terrain) if surface_terrain is not None else None}