__author__ = 'guiand1'



def build_vector(input_data, vector_data):
	if input_data is None:
		return [0] * len(vector_data)
	else:
		vect = [1 if item in input_data else 0 for item in vector_data]
		return vect


def convert_to_int(input_data, vector_data):
	if input_data is None:
		return None
	else:
		return vector_data.index(input_data)


def convert_cepage(input_data):
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
	return build_vector(input_data, cepages)


def convert_aromes(input_data):
	tab = ['Epicee', 'Florale', 'Fruitee', 'Boisee', 'Empyreumatique', 'Vegetale', 'Animale',
			 'Balsamique', 'Minerale']
	return build_vector(input_data, tab)


def convert_tannins(input_data):
	tab = ['Souples', 'Fermes', 'Charnus', 'Rudes']
	return convert_to_int(input_data, tab)


def convert_pastille(input_data):
	tab = ['Aromatique et charnu', 'Aromatique et souple', 'Fruite et genereux',
			 'Fruite et leger', 'Fruite et extra-doux']
	return convert_to_int(input_data, tab)


def convert_corps(input_data):
	tab = ['Leger', 'Moyen', 'Corse']
	return convert_to_int(input_data, tab)


def convert_texture(input_data):
	tab = ['Mince', 'Onctueuse', 'Ample', 'Grasse']
	return convert_to_int(input_data, tab)


def convert_sucre(input_data):
	tab = ['Sec', 'Demi', 'Doux']
	return convert_to_int(input_data, tab)


def convert_acidite(input_data):
	tab = ['Faible', 'Rafraichissante', 'Vive']
	return convert_to_int(input_data, tab)