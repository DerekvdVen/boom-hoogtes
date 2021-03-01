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

import zipfile



def get_directory_data_names(directory):
    load_list = []
    
    for tif in sorted(os.listdir(directory)):
        #print(tif)
        
        if str(tif).upper().endswith("ZIP"):
            pass
        
        elif str(tif).lower().endswith("tif"):
            load_list.append(tif)
        
        if not load_list:
            print('The tif directory seems to be empty, make sure to put DSMs in directory')
    return(load_list)

def DSM_DTM_list_to_CHM(DTM_list,DSM_list):


    for dtm, dsm in zip(DTM_list,DSM_list):
        # load DTM tile as array
        DTM = rasterio.open("./data/DTMs/" + dtm)
        DSM = rasterio.open("./data/DSMs/" + dsm)
        array = DTM.read()

        # fill empty
        msk = DTM.dataset_mask()
        DTM_filled = rasterio.fill.fillnodata(array, msk)

        # calculate CHM
        CHM = DSM.read() - DTM_filled
        CHM[CHM<0] = 0

        kwargs = DTM.meta # Copy metadata of rasterio.io.DatasetReader
        save_name = str(DTM).split("_")[1].split(".")[0] + "_CHM.tif"
        print(save_name, "saved")

        with rasterio.open('./data/CHMs/' + save_name, 'w', **kwargs) as file:
            file.write(CHM.astype(rasterio.float32))

def buffer_points(tree_points,buffersize_m=3):
    
    
    
    tree_points['geometry'] = tree_points.geometry.buffer(buffersize_m)
    return(tree_points)

def add_CHM_heights_to_points(CHM_list, identifier_column_name, tree_points):
    
    all_point_dataframe_list = []
    
    for chm in CHM_list:
        CHM = rasterio.open("data/CHMs/" + chm)

        affine = CHM.transform
        array = CHM.read(1)
        
        # To make sure the algorithm does not choose the null value, really large number, as max height
        array[array>9999] = 0

        tree_points_stats = tree_points.join(
            pd.DataFrame(
                zonal_stats(
                    vectors=tree_points.geometry, 
                    raster=array,
                    affine=affine,
                    stats=['max']
                )
            ),
            how='left'
        )
        
        # rename max column and remove points that are not calculated in the tile
        tree_points_stats = tree_points_stats.rename(columns={'max': 'Boomhoogte_ahn'})
        tree_points_stats = tree_points_stats[tree_points_stats.Boomhoogte_ahn.notnull()]
        
        
        tree_points_stats.drop(tree_points_stats.columns.difference([identifier_column_name,'Boomhoogte_ahn']), 1, inplace=True)
        
        all_point_dataframe_list.append(tree_points_stats)
    
    #
    all_point_dataframe = pd.concat(all_point_dataframe_list, ignore_index=True)
    
    return(all_point_dataframe)
        
def classify_heights_in_dataframe(dataframe):
    
    dataframe = pd.DataFrame(dataframe)
    
    labels = ['tot en met 5 m.','5-9 m.','9-12 m.', '12-15 m.','15-18 m.','18-21 m.', '21-24 m.', '24m. en hoger']
    
    dataframe["Boomhoogte"] = pd.cut(dataframe.Boomhoogte_ahn, [0,5,9,12,15,18,21,24,9999], right=False, labels=labels)
    
    return(dataframe)

