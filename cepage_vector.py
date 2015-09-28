__author__ = 'guiand1'


import numpy as np


def build(input_data):
	vect = np.zeros((1, 162))
	cepages = ['Mencia', 'Tempranillo',  'Barbera',  'Nero d''Avola',  'Corvina',  'Grenache',  'Mourvedre',  'Shiraz',
				  'Zinfandel',  'Nielluccio',  'Pinot noir',  'Cabernet-sauvignon',  'Syrah',  'Carignan',  'Malbec',
				  'Sangiovese',  'Tinta de Toro',  'Merlot',  'Monastrell',  'Ciliegiolo',  'Petite sirah',  'Mazuelo',
				  'Petit verdot',  'Marselan',  'Cabernet franc',  'Cabernet',  'Rondinella',  'Bonarda',  'Viognier',
				  'Canaiolo',  'Tinta roriz',  'Touriga Franca',  'Touriga nacional',  'Nebbiolo',  'Corvinone',
				  'Alicante Bouschet',  'Cinsault',  'Cannonau',  'Primitivo',  'Touriga francesa',  'Carmenere',
				  'Tinta barroca',  'Tannat',  'Sangiovese grosso',  'Negroamaro',  'Alicante Nero',  'Montepulciano',
				  'Graciano',  'Pinotage',  'Listan Negro',  'Tintilia',  'Saperavi',  'Croatina',  'Oseleta',  'Dolcetto',
				  'Gamay',  'Cot',  'Negrette',  'Grenache noire',  'Braucol (Fer)',  'Clairette',  'Sciacarello',
				  'Malvasia Nera',  'Aragonez',  'Frontenac',  'Marquette',  'Durif',  'Aglianico',  'Trousseau',
				  'De Chaunac',  'Marechal Foch',  'Sainte-Croix',  'Baco noir',  'Counoise',  'Chardonnay',  'Duras',
				  'Alfrocheiro',  'Abouriou',  'Molinara',  'Ancellotta',  'Pelaverga',  'Riesling',  'Cornalin',
				  'Fumin',  'Petit rouge',  'Vien de Nus',  'Saint-Laurent',  'Trincadeira',  'Cesar',  'Poulsard',
				  'Blaufrankisch',  'Castelao',  'Pinenc',  'Alicante',  'Bovale sardo',  'Colorino',  'Mondeuse',
				  'Lacrima',  'Garnacha tintorera',  'Refosco',  'Nerello Mascalese',  'Teroldego',  'Ruche',  'Bobal',
				  'Souzao',  'Tinta amarela',  'Nerello Capuccio',  'Monica',  'Jaen',  'Lucie Kuhlmann',
				  'Ruby cabernet',  'Frappato',  'Rossignola',  'Tinta francisca',  'Nero di Troia',  'Xinomavro',
				  'Zweigelt',  'Caberlot',  'Callet',  'Caladoc',  'Muscat noir',  'Tinto fino',  'Agiorgitiko',
				  'Pelaverga Piccolo',  'Feteasca Neagra',  'Baga',  'Castelao nacional',  'Albarossa',
				  'Jurancon noir (dame noir)',  'Diolinoire',  'Muscat',  'Limnio',  'Groslot',  'Semillon',
				  'Carcajolo nero',  'Vaccarese noir',  'Pineau d''Aunis',  'Maturana tinta',  'Freisa',
				  'Prugnolo gentile',  'Grand noir',  'Okuzgozu',  'Sabrevois',  'Gaglioppo',  'Kotsifali',
				  'Piedirosso',  'Mavrodaphne',  'Casavecchia',  'Pallagrello nero',  'Touriga cao',  'Saint Macaire',
				  'Pedro Ximenez',  'Tinta Cao',  'Camarate',  'Tinta Miuda',  'Barca (Tinta de Barca)',  'Mavrud',
				  'Trajadura',  'Kalavrytino',  'Kekfrancos',  'Castellan',  'Sagrantino']

	for i in xrange(162):
		cepage = cepages[i]
		if cepage in input_data:
			vect[i] = 1

	vect2 = [1 for cepage in cepages if cepage in input_data]

	return vect, vect2