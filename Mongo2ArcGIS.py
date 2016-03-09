##import urllib2
##import json
from key import MongoConnection
##import arcpy
print ('ok arcgis')

db = MongoConnection.getConnection()
print ('ok connection')


def printTwitterMessages():
    cursor = db.timeLine.find({ 'place': {'$ne': None} })
    num = 0
    print ('starting cursor')
    for s in cursor:

        place = s['place']

        placeName = place['full_name']
        bbox = place['bounding_box']
        coords =bbox['coordinates']
        wktGeometry = getWKTPolygon(coords)
        print('place %i: %s - %s' %(num, placeName, wktGeometry))

        num = num + 1
        if (num > 1000):
            break;


def getWKTPolygon(bbox):
    coords =bbox[0]
    wktText = 'POLYGON (( '
    for n in coords:
        ctext = ' %s, %s ' % (n[0], n[1])
        wktText = wktText + ctext
    wktText = wktText + ' ))'
    return wktText

if __name__ == "__main__":

    printTwitterMessages()
