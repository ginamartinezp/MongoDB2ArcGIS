from DataAccess import MongoDB
from DataAccess import Objects2GDB
import sys

db = MongoDB.getDB()
coll = MongoDB.getCollection()
collection_places = MongoDB.getCollectionName()
# fc_twitterPlaces = 'twitterplaces'
fc_points =Objects2GDB.fclasPoints
fc_polyline = Objects2GDB.fclasPolyline

# #This method aggregates all tweets' places that are stored in a defined collection
# #Into an ArcGIS FeatureClass
# def aggregateTwitterPlaces(coll, fc):
#     fields = ['full_name', 'country', 'place_type', 'country_code', 'name', 'count', 'SHAPE@']
#     cursor = db[coll].group( ['place' ], None, {'count': 0 },'function( curr, result){ result.count += 1;}')
#     objs = []
#     for res in cursor:
#         count = res['count']
#         try:
#             full_name = res['place']['full_name']
#         except:
#             full_name = 'null'
#
#         if full_name != 'null':
#             obj = []
#             obj.append(full_name)
#             obj.append(res['place']['country'])
#             obj.append(res['place']['place_type'])
#             obj.append(res['place']['country_code'])
#             obj.append(res['place']['name'])
#             obj.append(int(count))
#             bbcox = res['place']['bounding_box']
#             coords = bbcox['coordinates'][0]
#             geometry = Objects2GDB.getEsriPolygon(coords)
#             obj.append(geometry)
#             objs.append(obj)
#         print ('%s - %s Tweets' % (full_name, count))
#     Objects2GDB.insertObjects(fc_twitterPlaces, fields, objs)


def getGPSpoints(coll, lon, lat):
    fields=['name','time','precision','SHAPE@']
    cur=db[coll].find()
    count = 0
    for res in cur:
        obj = []
        longitude = res[lon]
        latitude = res[lat]
        geometry=Objects2GDB.getEsriPoint(longitude,latitude)
        #geometry = (longitude,latitude)
        obj.append(str(res['device']))
        obj.append(res['time_gps'])
        obj.append(res['precision'])
        obj.append(geometry)
        Objects2GDB.insertPoint(fc_points, fields, obj)
        count +=1
    print('Inserted %i objects '% (count))
    del cur

def getPolylineTracks(coll,lon, lat):
    fields=['name','time','precision','SHAPE@']
    cur=db[coll].aggregate (
        [
            {
              "$match":{"device": "be69c01dd9603be8", "longitude": { "$gt": -0.176, "$lt": 0.049 },
                            "latitude": { "$gt": 39.92, "$lt": 40.079 },
                            "speed": {"$lt":30}
                            }
            },
            {
              "$group": {
                "_id": {"device": "$device", "timestamp": "$time_gps"},
                "lat": { "$min": "$latitude"},
                "lon": {"$min": "$longitude"},
                "precision": {"$min": "$precision"},
                "count": {"$sum": 1}
              }

            },
            {
            "$sort": {"_id.device": 1, "_id.timestamp":-1,}
            },
            {
             "$limit": 1000
            }
        ]
    )
    count = 0
    objs=[]
    polylinePoints = []
    for res in cur:

        longitude = res['lon']
        latitude = res['lat']
        point = [longitude,latitude]
        polylinePoints.append(point)
    del cur
    obj = []
    geometry = Objects2GDB.getEsriPolyline(polylinePoints)
    obj.append(str(res['_id']['device']))
    obj.append(res['_id']['timestamp'])
    obj.append(res['precision'])
    obj.append(geometry)
    objs.append(obj)
    Objects2GDB.insertObjects(fc_polyline, fields, objs)
    count +=1
    print('Inserted %i objects '% (count))


    # cur1 = db[coll].distinct("device")
    # for c in cur1:
    #     cur2 = db[coll].find({"device": cur1[c]}) #"device": values stored in cur1
    #     count = 0
    #     objs = []
    #     polylinePoints = []
    #     for res in cur:
    #         longitude = res[lon]
    #         latitude = res[lat]
    #         point = [longitude, latitude]
    #         polylinePoints.append(point)
    #     del cur
    #     obj = []
    #     geometry = Objects2GDB.getEsriPolyline(polylinePoints)
    #     obj.append(str(res['device']))
    #     obj.append(res['time_gps'])
    #     obj.append(res['precision'])
    #     obj.append(geometry)
    #     objs.append(obj)
    #     Objects2GDB.insertObjects(fc_polyline, fields, objs)
    #     count += 1
    #     print('Inserted %i objects ' % (count))




#
# def printTwitterMessages():
#
#     cursor = coll.find({ 'place': {'$ne': None} })
#     num = 0
#     print ('starting cursor')
#     for s in cursor:
#
#         place = s['place']
#
#         placeName = place['full_name']
#         bbox = place['bounding_box']
#         coords =bbox['coordinates']
#         wktGeometry = getWKTPolygon(coords)
#         print('place %i: %s - %s' %(num, placeName, wktGeometry))
#
#         num = num + 1
#         if (num > 100):
#             break;
#
#
# def getWKTPolygon(bbox):
#     coords =bbox[0]
#     wktText = 'POLYGON (( '
#     for n in coords:
#         ctext = ' %s, %s ' % (n[0], n[1])
#         wktText = wktText + ctext
#     wktText = wktText + ' ))'
#     return wktText
#
if __name__ == "__main__":

    #aggregateTwitterPlaces('timeLine', 'p')

    #getGPSpoints(collection_places, "longitude", "latitude")

    getPolylineTracks(collection_places, "longitude", "latitude")

