# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 21:14:05 2016

@author: bipin
"""
import numpy as np
from osgeo import gdal
from osgeo import osr
from gdalconst import *

def operation1(b1,b2,b3):
    b_out = (b1+b2)/b3
    return b_out
    
def get_raster_band(file_name):
    'get band 1 from each file as a numpy array'''    
    f1 = gdal.Open(file_name,GA_ReadOnly)
    b1 = f1.GetRasterBand(1)    
    band_data = b1.ReadAsArray()
    return band_data,f1
    
def write_raster_band(filename,data1,transform,crs):    
    '''write data1 to file with filename filename , geotransform transform and projection crs'''
    data1 = np.array(data1)
    (rows,cols) = np.shape(data1)         
    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(filename, cols, rows, 1, gdal.GDT_Byte)    
    outRaster.SetGeoTransform(transform)
    outRaster.SetProjection(crs)    
    outband = outRaster.GetRasterBand(1)    
    outband.WriteArray(np.array(data1)) 
    outband.FlushCache()
    
    
def operator(operation,b1,b2,b3):
    '''applay operator along rows and coloums of the data'''
    return map(lambda x1,x2,x3 : map(operation,x1,x2,x3),b1,b2,b3)
    
    
if __name__ == '__main__':
    b1,f1 = get_raster_band('BAND2.tif')
    b2,f2 = get_raster_band('BAND3.tif')
    b3,f3 = get_raster_band('BAND4.tif')
    
    #b4 = operator(operation1,b1,b2,b3)
    b4 = (b1+b2)/b3
    write_raster_band('BAND_out.tif',b4,f1.GetGeoTransform(),f1.GetProjectionRef())
    
    
    
    
    
    
    
    
