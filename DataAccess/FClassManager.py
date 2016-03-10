import arcpy
import GDBAccess

wks = GDBAccess.getArcGISWorkspace()
arcpy.env.workspace = GDBAccess.gdb

def clearFeatureClass(fc):
    try:
        rows = arcpy.UpdateCursor(fc, "", "", "", "")
        for row in rows:
            rows.deleteRow(row)
        del rows
    except Exception as e:
        print ("Error Clearing FC: %s - %s" % (fc, e))

if __name__ == '__main__':
    print ("This is the manager for Feature Classes")

    fc = 'points'
    clearFeatureClass(fc)
