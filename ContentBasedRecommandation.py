# -*- coding: utf-8 -*-

__author__ = 'guiand1'

from pymongo import MongoClient
from pymongo import errors as pymongoerrors
from bson.objectid import ObjectId
from bunch import bunchify
import StringToIntVect as Stv
import numpy as np


def distance(xin, yin, weight, norm):
    if xin is None or yin is None:
        return 0, 0
    else:
        return weight * abs(xin - yin) / norm, weight


def compute_correlation(x1, x2):
    x = np.asarray(x1)
    y = np.asarray(x2)
    mx = x.mean()
    my = y.mean()
    xm, ym = x - mx, y - my
    r_num = np.add.reduce(xm * ym)
    r_den = np.sqrt(np.sum(xm * xm, 0) * np.sum(ym * ym, 0))
    if r_den > 0:
        return r_num / r_den, 1
    else:
        return 0, 0


def score(wine_a, wine_b):
    # Weights [cepage, gout, nez, distance, format, alcool]
    weights = np.array([5., 1., 1., 2., 10., 3.], dtype=np.float32)
    corr_weights = np.array([1.] * 6, dtype=np.float32)
    # Coefficients
    coeff = np.array([1.] * 6, dtype=np.float32)
    # Correlation cepage
    coeff[0], corr_weights[0] = compute_correlation(wine_a.cepage_int, wine_b.cepage_int)
    # Correlation aromes gout
    coeff[1], corr_weights[1] = compute_correlation(wine_a.gout_int, wine_b.gout_int)
    # Correlation aromes gout
    coeff[2], corr_weights[2] = compute_correlation(wine_a.nez_int, wine_b.nez_int)
    weights = weights * corr_weights
    # Distance
    wi = np.array([0.] * 6, dtype=np.float32)
    dist = np.array([0.] * 6, dtype=np.float32)
    nbtannin = 3.
    nbpastille = 5.
    nbcorps = 3.
    nbtexture = 4.
    nbsucre = 3.
    nbacidite = 3.
    dist[0], wi[0] = distance(wine_a.tannins_int, wine_b.tannins_int, 1., nbtannin)
    dist[1], wi[1] = distance(wine_a.pastilleGout_int, wine_b.pastilleGout_int, 5., nbpastille)
    dist[2], wi[2] = distance(wine_a.corps_int, wine_b.corps_int, 2., nbcorps)
    dist[3], wi[3] = distance(wine_a.texture_int, wine_b.texture_int, 1., nbtexture)
    dist[4], wi[4] = distance(wine_a.sucre_int, wine_b.sucre_int, 2., nbsucre)
    dist[5], wi[5] = distance(wine_a.acidite_int, wine_b.acidite_int, 1., nbacidite)
    if sum(wi) == 0:
        coeff[3] = 0
        weights[3] = 0
    else:
        coeff[3] = -sum(dist) / sum(wi)
    # Format
    coeff[4] = -abs(wine_a.format - wine_b.format) / (wine_a.format + wine_b.format)
    # Alcool
    # if(wine_a._id == ObjectId("55f8651491653105d04a2cb2") and wine_b._id == ObjectId("55f8651491653105d04a3681")):
    #     toto = 2
    print "id1: {0} et id2: {1}".format(wine_a._id, wine_b._id)
    if wine_a.alcool is None or wine_b.alcool is None:
        weights[5] = 0
    else:
        coeff[5] = -abs(wine_a.alcool - wine_b.alcool) / (wine_a.alcool + wine_b.alcool)

    return 100 * weights.dot(coeff) / np.sum(weights)


def find_top_ten(wine_in):
    wine_in.correlation.sort(key=lambda item: item[1], reverse=True)
    nbwine = 0
    topten = []
    for wineitem in wine_in.correlation:
        if wineitem[0] == wine_in._id:
            continue
        else:
            topten.append(wineitem)
            nbwine += 1
        if nbwine == 10:
            break
    return topten


def compute_top_ten():
    # Get credentials
    with open('credentials.json') as data_file:
        credentials = json.load(data_file)
    # Connection with MongoClient
    uri = 'mongodb://{0}:{1}@{2}:{3}/{4}'.format(credentials.username, credentials.pwd,
                                                 credentials.url, credentials.port, credentials.bd)
    # Connection with MongoClient
    client = MongoClient(uri)
    # Getting database
    db = client.SaqRecommandation
    # Getting collection
    collection = db.wines
    list_of_wines = [bunchify(wine) for wine in collection.find({})]

    for wine in list_of_wines:
        wine.cepage_int = Stv.convert_cepage(wine.cepage)
        wine.gout_int = Stv.convert_aromes(wine.gout)
        wine.nez_int = Stv.convert_aromes(wine.nez)
        wine.tannins_int = Stv.convert_tannins(wine.tannins)
        wine.pastilleGout_int = Stv.convert_pastille(wine.pastilleGout)
        wine.corps_int = Stv.convert_corps(wine.corps)
        wine.texture_int = Stv.convert_texture(wine.texture)
        wine.sucre_int = Stv.convert_sucre(wine.sucre)
        wine.acidite_int = Stv.convert_acidite(wine.acidite)

    for wine in list_of_wines:
        # if not wine.nom == 'Jose Maria da Fonseca Periquita Reserva':
        #     continue
        wine.correlation = None
        for wine2 in list_of_wines:
            wine.correlation.append((wine2._id, score(wine, wine2)))
        wine.top_ten = find_top_ten(wine)
        try:
            wine_to_update = collection.find_one({"_id": wine._id})
            wine_to_update["top_ten"] = []
            if wine_to_update is not None:
                for winetop in wine.top_ten:
                    wine_to_update["top_ten"].append({'_id': winetop[0], 'corr': float(winetop[1])})
            collection.update({"_id": wine_to_update['_id']}, wine_to_update)
        except pymongoerrors.PyMongoError:
                print 'An error has occured, retry...'
                continue

# *****************************************
# Main called function
# *****************************************
if __name__ == '__main__':
    compute_top_ten()
