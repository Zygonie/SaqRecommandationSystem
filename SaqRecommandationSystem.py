# -*- coding: utf-8 -*-

__author__ = 'guillaume'

import requests as http
import re  # regular expression
import bs4 as BeautifulSoup
import json
import os
import unicodedata
from pymongo import MongoClient
from pymongo import errors as PyMongoErrors
from io_saq import jdefault
from io_saq import save_list_to_mongo
from ContentBasedRecommandation import compute_top_ten


# *****************************************
# Definition of the class WineItem
# *****************************************
class WineItem:
    def __init__(self):
        self.url = None
        self.name = None
        self.codeSAQ = None
        self.prix = None
        self.format = None
        self.pastilleGout = None
        self.couleur = None  # rouge, blanc, rose
        self.pays = None
        self.region = None
        self.alcool = None
        self.nez = []
        self.gout = []
        self.acidite = None
        self.sucre = None
        self.tannins = None
        self.texture = None
        self.corps = None
        self.cepage = None
        self.top_ten = []

    def to_json(self):
        seriazable_object = self.__dict__
        # other method : json.dumps(newWine, indent=4, default=jdefault) #default(obj) is a function that should return
        # a serializable version of obj or raise TypeError
        # where def jdefault(o) : return o.__dict__
        return json.dumps(seriazable_object, indent=4)


# *****************************************
# Get the list of wines
# *****************************************
def get_list_of_wines(nbitems=200):
    mylist = []

    if os.path.exists('listOfWines.json'):
        os.remove('listOfWines.json')

    if os.path.exists('sourceAllWines.html'):
        with open('sourceAllWines.html', mode='r') as file:
            html = unicodedata.normalize('NFKD', file.read().decode('utf-8')).encode('ASCII', 'ignore')
            source_site_code = BeautifulSoup.BeautifulSoup(html)
    else:
        # Ouverture de la page web
        url = u'http://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?searchType=&categoryIdentifier=0602&'\
                'showOnly=product&langId=-2&pageSize=' + str(nbitems) +'&catalogId=50000&storeId=20002'
        request = http.get(url)
        html = request.text  # .decode('utf-8')
        html = unicodedata.normalize('NFKD', html).encode('ASCII', 'ignore')
        source_site_code = BeautifulSoup.BeautifulSoup(html)
        with open('sourceAllWines.html', mode='w') as file:
            file.write(html)

    # re.compile pour utiliser une expression reguliere avec la methode 'match'.
    # Ici on cherche tous les div dont l'id contient 'result'
    results = source_site_code.find_all('div', id=re.compile('result_'), attrs={'class': u'resultats_product'})

    with open('listOfWines.json', mode='a') as outfile:
        # outfile.write('[')
        for result in results:
            new_wine = WineItem()
            nom_section = result.find('p', attrs={'class': u'nom'})
            # url
            new_wine.url = nom_section.a['href']
            # nom
            new_wine.nom = nom_section.a.text
            # format
            sectiondescr = result.find('p',  attrs={'class': u'desc'}).text
            sectiondescr = unicodedata.normalize('NFKC', sectiondescr.encode('utf-8', 'ignore').
                                                 decode('utf-8', 'ignore')).encode('ASCII', 'ignore')
            m = re.findall('(\d+\,?\d*)', sectiondescr)
            format_bouteile = m[0]
            format_bouteile = format_bouteile.replace(',', '.')
            new_wine.format = float(format_bouteile)
            # code SAQ
            new_wine.codeSAQ = m[len(m)-1]
            # pastille de gout
            section_flavor = result.find('p',  attrs={'class': u'flavor'})
            if section_flavor.img is not None:
                image_title = section_flavor.img['title']
                m = re.findall(r'(\b[^\s]+\b)', image_title)
                new_wine.pastilleGout = ''
                gout_idx = m.index(u'gout')
                new_wine.pastilleGout = ' '.join(word for word in m[gout_idx+1:])
            # prix
            price_txt = result.find('td',  attrs={'class': u'price'}).a.text
            price_txt = price_txt.replace(' ', '')
            price_txt = price_txt.replace('$', '')
            price_txt = price_txt.replace(',', '.')
            new_wine.prix = float(price_txt)
            # append to file
            mylist.append(new_wine)
            # outfile.write('{0},{1}'.format(newWine.ToJson(), os.linesep))
        # outfile.write(']')
        json.dump(mylist, outfile, default=jdefault, indent=4)


# *****************************************
# Update MongoDB database with wine descriptions
# *****************************************
def get_wine_description():
    # Get credentials
    with open('credentials.json') as data_file:
        credentials = json.load(data_file)
    # Connection with MongoClient
    uri = 'mongodb://{0}:{1}@{2}:{3}/{4}'.format(credentials.username, credentials.pwd,
                                                 credentials.url, credentials.port, credentials.bd)
    client = MongoClient(uri)
    # Getting database
    db = client.SaqRecommandation
    # Getting collection
    collection = db.wines
    for wine in collection.find():
        try:
            if wine['couleur'] is None:
                parse_data_descr_from_web(wine)
                collection.update({"_id": wine['_id']}, wine)
                print 'id {0} updated'.format(wine['_id'])
        except PyMongoErrors.PyMongoError as e:
            print e.message
            if hasattr(e, 'errno') and hasattr(e, 'strerror'):
                print "MongodB error({0}): {1}".format(e.errno, e.strerror)


# *****************************************
# Parse wine details from URL
# *****************************************
def parse_data_descr_from_web(wine):
    # Ouverture de la page web
    url = wine['url']
    request = http.get(url)
    html = request.text  # .decode('utf-8')
    html = unicodedata.normalize('NFKD', html).encode('ASCII', 'ignore')
    source_site_code = BeautifulSoup.BeautifulSoup(html)
    section_details = source_site_code.find('div', attrs={'id': u'details'})
    section_tasting = source_site_code.find('div', attrs={'id': u'tasting'})

    wine['couleur'] = None
    wine['pays'] = None
    wine['cepage'] = []
    wine['region'] = None
    wine['alcool'] = None
    wine['nez'] = []
    wine['acidite'] = None
    wine['tannins'] = None
    wine['sucre'] = None
    wine['texture'] = None
    wine['corps'] = None
    wine['gout'] = []

    if section_details is not None:
        couleur_str = section_details.find(text='couleur')
        if couleur_str is not None:
            div_couleur = couleur_str.find_parent('div').find_next_sibling('div', attrs={'class': 'right'})
            if div_couleur is not None:
                m = re.search('(\w+)', div_couleur.text)
                wine['couleur'] = m.group(1)
        pays_str = section_details.find(text=u'Pays')
        if pays_str is not None:
            div_pays = pays_str.find_parent('div').find_next_sibling('div', attrs={'class': 'right'})
            if div_pays is not None:
                m = re.search('(\w+)', div_pays.text)
                wine['pays'] = m.group(1)
        cepage_str = section_details.find(text=u'Cepage(s)')
        if cepage_str is not None:
            div_cepage = cepage_str.find_parent('div').find_next_sibling('div', attrs={'class': 'right'})
            if div_cepage is not None:
                for line in div_cepage.find_all('tr'):
                    cepage = line.find('td').text
                    wine['cepage'].append(cepage)
        region_str = section_details.find(text=u'Region')
        if region_str is not None:
            div_region = region_str.find_parent('div').find_next_sibling('div', attrs={'class': 'right'})
            if div_region is not None:
                m = re.search('(?:\r|\n|\s)*([\w\s-]*\w)(?:\r|\n|\s)', div_region.text)
                wine['region'] = m.group(1)
        alcool_str = section_details.find(text=u"Degre d'alcool")
        if alcool_str is not None:
            alcool_txt = alcool_str.find_parent('div').find_next_sibling('div', attrs={'class': 'right'}).text
            alcool_txt = alcool_txt.replace(' ', '')
            alcool_txt = alcool_txt.replace('%', '')
            alcool_txt = alcool_txt.replace(',', '.')
            wine['alcool'] = float(alcool_txt)
        if section_tasting is not None:
            div_olfactif = section_tasting.find('div', attrs={'class': 'olfactives'})
            list_olfactif = div_olfactif.find_all('li')
            for odeur in list_olfactif:
                wine['nez'].append(odeur.text)
            div_gustative = section_tasting.find('div', attrs={'class': 'gustatives'})
            span_acidite = div_gustative.find('span', text='Acidite :')
            if span_acidite is not None:
                m = re.search('(\w+)', span_acidite.next_sibling)
                wine['acidite'] = m.group(1)
            span_tannin = div_gustative.find('span', text='Tannins :')
            if span_tannin is not None:
                m = re.search('(\w+)', span_tannin.next_sibling)
                wine['tannins'] = m.group(1)
            span_sucre = div_gustative.find('span', text='Sucre :')
            if span_sucre is not None:
                m = re.search('(\w+)', span_sucre.next_sibling)
                wine['sucre'] = m.group(1)
            span_texture = div_gustative.find('span', text='Texture :')
            if span_texture is not None:
                m = re.search('(\w+)', span_texture.next_sibling)
                wine['texture'] = m.group(1)
            span_corps = div_gustative.find('span', text='Corps :')
            if span_corps is not None:
                m = re.search('(\w+)', span_corps.next_sibling)
                wine['corps'] = m.group(1)
            div_aromes = section_tasting.find('div', text="Familles d'aromes :")
            list_aromes = div_aromes.parent.find_all('li')
            for arome in list_aromes:
                wine['gout'].append(arome.text)


# *****************************************
# Main called function
# *****************************************
if __name__ == '__main__':
    get_list_of_wines(7000)
    save_list_to_mongo()
    get_wine_description()
    compute_top_ten()
    print "Finished!"