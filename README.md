# boom-hoogtes

The purpose of this collection of scripts is to add height information to tree points. To run the workflow.bat, you will need to install a conda environment manager (miniconda for example). You may start the workflow by running FME_batch.fmw. For this you will need to install FME. 

The workflow can also be called from the shell:

.\workflow.bat $(anaconda_loc) $(polygon_file_location) $(identifier_column_name) $(layer)
  OPTIONAL $(buffer_size)
  
                # anaconda3_location=C:\Users\Derek\Anaconda3 , location to check for conda environment
                # polygon_file_location=data/polygon_input/shapefile.sh, shapefile location
                # identifier_column_name=KRcode, object id column name
                # layer=pGroen, laag in geodatabase naam = pGroen
                # buffer_size, buffers om boom punten om hoogste punt te pakken = 4
                
                
 This directory contains 4 scripts:

-- workflow.bat
    batch file to call all other scripts in the order as shown below
    also installs all modules in conda environment

-- FME_batch.fmw
    simply calls the workflow.bat with a popup for user parameters.
    
-- boomhoogtes_from_ahn.py
    input:
        - ESRI geodatabase, point layer 
        - DSM and DTM from for example: https://downloads.pdok.nl/ahn3-downloadpage/ 
            STORED IN data/DSMs and data/DTMs
    output:
        - output/Tree_heights_KR_code.xlsx

-- functions.py
    contains functions for running boomhoogtes_from_ahn.py
