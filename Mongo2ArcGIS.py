from DataAccess import MongoDB
from DataAccess import Objects2GDB

db = MongoDB.getDB()
coll = MongoDB.gedCollection()
fc_twitterPlaces = 'twitterplaces'

#This method aggregates all tweets' places that are stored in a defined collection
#Into an ArcGIS FeatureClass
def aggregateTwitterPlaces(coll, fc):
    fields = ['full_name', 'country', 'place_type', 'country_code', 'name', 'count', 'SHAPE@']
    cursor = db[coll].group( ['place' ], None, {'count': 0 },'function( curr, result){ result.count += 1;}')
    objs = []
    for res in cursor:
        count = res['count']
        try:
            full_name = res['place']['full_name']
        except:
            full_name = 'null'

        if full_name != 'null':
            obj = []
            obj.append(full_name)
            obj.append(res['place']['country'])
            obj.append(res['place']['place_type'])
            obj.append(res['place']['country_code'])
            obj.append(res['place']['name'])
            obj.append(int(count))
            bbcox = res['place']['bounding_box']
            coords = bbcox['coordinates'][0]
            geometry = Objects2GDB.getEsriPolygon(coords)
            obj.append(geometry)
            objs.append(obj)
        print ('%s - %s Tweets' % (full_name, count))
    Objects2GDB.insertObjects(fc_twitterPlaces, fields, objs)






def printTwitterMessages():

    cursor = coll.find({ 'place': {'$ne': None} })
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
        if (num > 100):
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

    aggregateTwitterPlaces('timeLine', 'p')
