import arcpy

gdb = './Data/WKTGDB.gdb/' # ESRI Geodatabase Location
fclasPoints = 'points'
fclasPoints = 'gpsPoints'
fclasPolyline = 'polyline'
fclasPolygon = 'polygons'
wksp = arcpy.env.workspace = gdb


if __name__ == '__main__':
    ws = getArcGISWorkspace()
    print ("This is your workspace")
    print ws