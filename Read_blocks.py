#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 21:06:03 2017

@author: bipin
"""
from osgeo import gdal
from osgeo import osr
from osgeo.gdalconst import *
import numpy as np
import itertools as it
import struct

in_fn1 = 'BAND2.tif'
in_fn2 = 'BAND3.tif'
out_fn = 'out_band.tif'


    
    
def operate_blocks(b1,b2,out_b1,operation):
    [nx,ny] = b1.GetBlockSize()
    for blk_idx_x,blk_idx_y in it.product(range(b1.XSize/nx),range(b1.YSize/ny)):
        if b1.DataType == GDT_UInt16:
            blk1 = b1.ReadBlock(blk_idx_x,blk_idx_y)
            blk2 = b2.ReadBlock(blk_idx_x,blk_idx_y)
            dat1 = np.array(struct.unpack('H'*nx*ny,blk1))
            dat2 = np.array(struct.unpack('H'*nx*ny,blk2))
            #dat1.shape = [nx,ny]
            #dat2.shape = [nx,ny]
            #out = (dat2/2 + dat1/2)
            out = map(operation,dat1,dat2)
            packed_data = out.astype(np.uint16).tostring()
            out_b1.WriteRaster(blk_idx_x*nx,blk_idx_y*ny,nx,ny,packed_data)
            out_b1.FlushCache()

def operation(d1,d2):
    return d1/2+d2/2

if __name__ == '__main__':
    f1 = gdal.Open(in_fn1,GA_ReadOnly)
    f2 = gdal.Open(in_fn2,GA_ReadOnly)
    driver = f1.GetDriver()
    f_out = driver.CreateCopy( out_fn , f1, 0 )
    f_out = None
    f_out = gdal.Open(out_fn,GA_Update)
    b1 = f1.GetRasterBand(1)
    b2 = f2.GetRasterBand(1)
    out_b1 = f_out.GetRasterBand(1)
    operate_blocks(b1,b2,out_b1,operation)
                
    
