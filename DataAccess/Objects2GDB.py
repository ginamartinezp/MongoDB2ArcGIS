import arcpy
import GDBAccess

gdb = GDBAccess.gdb
arcpy.env.workspace = gdb

gdb = GDBAccess.gdb
fclasPoints = GDBAccess.fclasPoints
fclasPolyline = GDBAccess.fclasPolyline
fclasPolygon = GDBAccess.fclasPolygon

def getEsriPoint (cx, cy):
    point = arcpy.Point(cx, cy)
    return point

def getEsriPolygon(pts):
    polygon = arcpy.Polygon(arcpy.Array([arcpy.Point(*p) for p in pts]))
    return polygon

def getEsriPolyline(pts):
    polyline = arcpy.Polyline(arcpy.Array([arcpy.Point(*p) for p in pts]))
    return polyline

def insertObjects(fc, fields, objs):
    cursor = arcpy.da.InsertCursor(gdb + fc, fields)
    for o in objs:
        try:
            cursor.insertRow(o)
        except Exception as e:
            print (repr(e))

    del cursor

#Function to optmize the process to insert points
def insertPoint(fc, fields, point):
    cursor = arcpy.da.InsertCursor(gdb + fc, fields)
    try:
        cursor.insertRow(point)
    except Exception as e:
        print(e)
    del cursor


if __name__ == '__main__':
    fields = ['name', 'description', 'SHAPE@']

    objs = []
    name = 'yo'
    description = 'Soy yo'
    cx = 40.00
    cy = -0.1
    point = getEsriPoint(cx,cy)
    obj = (name,description,point)
    objs.append(obj)
    insertObjects(gdb+fclasPoints, fields, objs)
    print ('point inserted')

    objs1 = []
    polylinePoints = [[39.9, -0.1], [39.95,-0.1], [39.95, -0.05], [40.0, -0.05]]
    name = 'polyline'
    description = 'my poline'
    pline = getEsriPolyline(polylinePoints)
    obj = (name,description,pline)
    objs1.append(obj)
    insertObjects(gdb+fclasPolyline,fields,objs1)
    print ('polyline inserted')


    objs2 = []
    delay = 0.6
    name = 'polygon'
    description = 'my poligon'
    polygonPoints = [[39.9, -0.1], [39.85, -0.1], [39.85, -0.15], [39.9, -0.15]]
    polygon = getEsriPolygon(polygonPoints)
    obj = (name,description,polygon)
    objs2.append(obj)
    insertObjects(gdb+fclasPolygon,fields,objs2)
    print ('polygon inserted')


