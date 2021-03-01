@echo off

rem workflow.bat - Derek van de Ven - 26-2-2021

rem This workflow.bat runs a set of scripts to collect height information from DSMs and DTMs in the Netherlands for tree points. 
rem Inputs are the anaconda3 directory location, the geodatabase location, the (point) layer, and the identifier column name in the geodatabase:

rem FME parameters
rem # anaconda3_location=C:\Users\Derek\Anaconda3 , location to check for conda environment
rem # polygon_file_location=data/polygon_input/shapefile.sh, shapefile location
rem # identifier_column_name=KRcode, object id column name
rem # layer=pGroen, object id column name

rem Parameters
set anaconda3_location=%1
set polygon_file_location=%2
set identifier_column_name=%3
set layer=%4

rem Optional parameter
set buffer_size=%5

rem fixed parameter
set CONDA_ENV=\envs\conda_trees2

rem set name conda environment
set conda_polygons_location=%anaconda3_location%%CONDA_ENV%

if exist %conda_polygons_location% (
    echo "Conda environment already exists"
    
    rem update packages if environment already exists
    call conda activate conda_trees2
    call conda update --all -y
    call conda deactivate

) else (
    echo "Conda environment does not yet exist"
    call conda create --name conda_trees2 pandas geopandas rasterio matplotlib descartes shapely openpyxl rasterstats -y
)

rem run python script
call conda activate conda_trees2
python boomhoogtes_from_ahn.py %polygon_file_location% %identifier_column_name% %layer% %buffer_size%