# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "onetime"

import arcpy

arcpy.env.workspace = 'D:\\GISData\\ksbclc\\newnc\\test.gdb'

mxd = arcpy.mapping.MapDocument('D:\\GISData\\ksbclc\\newnc\\test.mxd')

#加原始文件
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
theShape = "onetime"
addLayer = arcpy.mapping.Layer(theShape)
arcpy.mapping.AddLayer(df, addLayer, "AUTO_ARRANGE")
#addLayer.maxScale = 250000.0-10000.0
#addLayer.minScale = 250000.0

#加坐标轴
sr = arcpy.SpatialReference("WGS 1984")
arcpy.DefineProjection_management('onetime', sr)

#加属性列
arcpy.AddField_management('onetime','level','TEXT')

#计算level
field="level"
in_table="onetime"
expression=r"addlevel( !xindex!,!yindex!)"
expression_type=r"PYTHON_9.3"
code_block="def addlevel(xindex,yindex):\n    levellist = '1'\n    if (xindex%2==0) and (yindex%2==0):\n        levellist+='2'\n        if (xindex%4==0) and (yindex%4==0):\n            levellist+='3'\n            if (xindex%8==0) and (yindex%8==0):\n                levellist+='4'\n                if (xindex%16==0) and (yindex%16==0):\n                    levellist+='5'\n                    if (xindex%32==0) and (yindex%32==0):\n                        levellist+='6'\n                        if (xindex%64==0) and (yindex%64==0):\n                            levellist+='7'\n                            if (xindex%128==0) and (yindex%128==0):\n                                levellist+='8'\n    return levellist"
arcpy.CalculateField_management(in_table, field, expression, expression_type, code_block)

#加图层
for i in range(2,9):
    in_features=r"onetime"
    out_layer="level{}".format(i)
    where_clause="level LIKE '%{}'".format(i)
    arcpy.MakeFeatureLayer_management(in_features, out_layer, where_clause)
    layer = arcpy.mapping.Layer(out_layer)
    arcpy.mapping.AddLayer(df, layer, "AUTO_ARRANGE")
    #layer.maxScale = float(250000*(2**(i-1))-10000)
    #layer.minScale = float(250000*(2**(i-1)))
    
#改可见比例尺范围
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.name == 'onetime':
        lyr.name = 'level1'
        lyr.minScale = 250000
    else:
        num = int(lyr.name.split('l')[-1])
        lyr.maxScale = 250000*(2**(num-1))
        lyr.minScale = 250000*(2**(num-1))
        if lyr.name == 'level8':
            lyr.minScale = 0
        
#刷新mxd保存
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
mxd.save()
