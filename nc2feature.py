# -*- coding: utf-8 -*-

import netCDF4
import numpy as np
import numpy.ma
import sys
import time
import datetime
import arcpy

sincedate = datetime.datetime.strptime('1990-01-01','%Y-%m-%d')
ncpath = r"D:\GISData\ksbclc\oldnc\nwp_current_20181113.nc"

ds = netCDF4.Dataset(ncpath, 'r', format='NETCDF4')
udata = ds.variables['u']
vdata = ds.variables['v']

#data type is maskedarray
uvaluedata = udata[:]
vvaluedata = vdata[:]

del udata
del vdata

#y
southnorthdata = ds.variables['lat'][:]
#x
westeastdata = ds.variables['lon'][:]
timedata = ds.variables['time'][:]

newudata = uvaluedata[:,:,:,:]
newvdata = vvaluedata[:,:,:,:]

#newudata = (newudata.round(1,None)==1.1)*1.1

f = np.array([[0.25,0.25],[0.25,0.25]])

if len(southnorthdata)%2 != 0:
    np.delete(southnorthdata,-1)
if len(westeastdata)%2 != 0:
    np.delete(westeastdata,-1)
newy = (southnorthdata[::2]+southnorthdata[1::2])/2
newx = (westeastdata[::2]+westeastdata[1::2])/2

datatype = np.dtype({'names':['time','y','x','u','v','yindex','xindex'],'formats':['i','f', 'f','f','f','i','i']})
resultarr = []

for t in range(len(timedata)):
    urow = uvaluedata[t,0,::2,:]+uvaluedata[t,0,1::2,:]
    
    newu = (urow[:,::2]+urow[:,1::2])/4
    vrow = vvaluedata[t,0,::2,:]+vvaluedata[t,0,1::2,:]

    newv = (vrow[:,::2]+vrow[:,1::2])/4
    
    time = (sincedate+datetime.timedelta(hours=int(timedata[t]))).strftime("%Y-%m-%d %H:%M:%S")
    for xindex in range(len(newx)):
        
        for yindex in range(len(newy)):
            
            resultrow = (timedata[t],newy[yindex],newx[xindex],newu[yindex,xindex],newv[yindex,xindex],yindex,xindex)
            resultarr.append(resultrow)
    print time
            
resultarr = np.array(resultarr,dtype=datatype)
print 'success'

arcpy.da.NumPyArrayToFeatureClass(resultarr, 'D:\\GISData\\ksbclc\\newnc\\points.shp', ('x','y'))
print 'success'

