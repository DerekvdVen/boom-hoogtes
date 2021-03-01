import os
import rasterio
from rasterio.plot import show
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from rasterstats import zonal_stats
from rasterio.fill import fillnodata
import fiona
from osgeo import ogr


import zipfile

from functions import get_directory_data_names, DSM_DTM_list_to_CHM, buffer_points, add_CHM_heights_to_points, classify_heights_in_dataframe

if not os.path.exists('data'): os.makedirs('data')
if not os.path.exists('data/DSMs'): os.makedirs('data/DSMs')
if not os.path.exists('data/DTMs'): os.makedirs('data/DTMs')
if not os.path.exists('data/CHMs'): os.makedirs('data/CHMs')
if not os.path.exists('data/geodatabase'): os.makedirs('data/geodatabase')
if not os.path.exists('output'): os.makedirs('output')


tree_point_location = "data/geodatabase/OMS_NHM_20201223.gdb"
gdb_layer = "pGroen"
# layerlist = fiona.listlayers(tree_point_location)
# print(layerlist)
tree_points = gpd.read_file(tree_point_location,layer=gdb_layer)

# get list of DTM and DSM names in directory
DTM_list = get_directory_data_names("data/DTMs")
print(DTM_list)
DSM_list = get_directory_data_names("data/DSMs")
print(DSM_list)

print(tree_points)
# get list of DTM and DSM names in directory
DTM_list = get_directory_data_names("data/DTMs")
DSM_list = get_directory_data_names("data/DSMs")


# create CHM from DSM and DTMs
DSM_DTM_list_to_CHM(DTM_list=DTM_list,DSM_list=DSM_list)


# buffer tree points
tree_point_buffers = buffer_points(tree_points, buffersize_m=4)


# get list of CHM names in directory
CHM_list = get_directory_data_names("data/CHMs")


# combine CHM heights with tree_point_buffer to gain height stats
tree_point_stats = add_CHM_heights_to_points(CHM_list=CHM_list, tree_points=tree_point_buffers)


# classify
data = classify_heights_in_dataframe(tree_point_stats)


data.to_excel("output/Tree_heights_KR_code.xlsx")

