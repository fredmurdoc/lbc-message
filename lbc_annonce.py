from bs4 import BeautifulSoup
import logging
import sys
from datetime import datetime
import urllib.parse
from lbc_message import LbcMessage
import re
import os.path
from lxml import etree

class LbcAnnonce():
    fp_html = None
    REGEXP_COMMUNE_CP= r'\s*(?P<commune>[^0-9]+)\s*(?P<cp>[0-9]{5})\s*'
    def __init__(self, html_file):
        self.fp_html = open(html_file, 'r')
        self.id_annonce = os.path.basename(html_file).replace(".htm", '')
        self.soup = BeautifulSoup(self.fp_html, features='lxml')
        if len(self.soup) == 0:
            raise Exception("file %s is empty" % self.fp_html.name)
        self.dom = etree.HTML(str(self.soup))
    
    def __del__(self):
        if self.fp_html is not None:
            self.fp_html.close()
            
    def est_desactivee(self):
        annonce_desactivee = self.soup.find(string='Cette annonce est désactivée')
        return annonce_desactivee is not None

    def extract_metadatas(self):
        p_data_annonce = self.soup.find('p', attrs={'data-qa-id' : "adview_date"})
        date_annonce = datetime.strptime(p_data_annonce.text, '%d/%m/%Y à %H:%M').strftime('%d/%m/%Y %H:%M') if p_data_annonce is not None else None
        p_data_commune = self.dom.xpath("//span[@href='#map']")
        logging.debug("p_data_commune : %s" % p_data_commune)
        commune, cp = None, None
        if p_data_commune is not None and len(p_data_commune) > 0:
            logging.debug('p_data_commune[0].text %s' % p_data_commune[0].text)
            m = re.search(self.REGEXP_COMMUNE_CP, p_data_commune[0].text)
            if m is not None:
                commune = m.group('commune')
                cp = m.group('cp')
        p_data_prix = self.soup.find('div', attrs={'data-qa-id' : "adview_price"})
        p_data_description = self.soup.find('div', attrs={'data-qa-id' : 'adview_description_container'})
        prix_annonce = int(p_data_prix.text.replace('€', '').replace(' ', '').replace('\u202f', '').replace('\u202f', '\xa0')) if p_data_prix is not None else None
        return { 'date_annonce' : date_annonce, 'prix': prix_annonce, 
                'description' : p_data_description.text if p_data_description is not None else None, 
                'commune': commune, 'code_postal': cp}

    def extract_criteres(self):
        criteres = self.soup.find(string='Critères')
        if criteres is None:
            return None
        divs_criteres = criteres.find_parent('div')
        logging.debug("divs_criteres")
        logging.debug(divs_criteres)
        spans_criteres = divs_criteres.find_all('span')
        logging.debug("spans_criteres")
        logging.debug(spans_criteres)
        version_with_div_criteres = divs_criteres.find_all('div', {'data-test-id':"criteria"})
        logging.debug("version_with_div_criteres")
        logging.debug(version_with_div_criteres)
        spans_criteres
        a_terrain = False
        surface, nb_pieces, type_maison, surface_terrain = [None, None, None, None]
        for span_critere in spans_criteres:
            logging.debug("span_critere : %s" % span_critere.text)
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
        for div_critere in version_with_div_criteres:
            logging.debug("div_critere : %s" % div_critere.text)

        for div_critere in version_with_div_criteres:
            if 'Type de bien' in div_critere.text:
                type_maison = div_critere.text.replace('Type de bien', '').lower()
            if 'Surface habitable' in div_critere.text:
                surface = div_critere.text.replace('Surface habitable', '').replace(' m\u00b2', '')
            if 'Nombre de pièces' in div_critere.text:
                nb_pieces = div_critere.text.replace('Nombre de pièces', '').replace(' pièce', '')
            if 'Surface totale du terrain'in div_critere.text:
                surface_terrain=div_critere.text.replace('Surface totale du terrain', '').replace(' m\u00b2', '')
                a_terrain = True
        return { 'a_terrain' : a_terrain,  'surface' : int(surface) if surface is not None else None, 'nb_pieces' : int(nb_pieces) if nb_pieces is not None else None , 'type_maison' : type_maison, 'surface_terrain' : int(surface_terrain) if surface_terrain is not None else None}