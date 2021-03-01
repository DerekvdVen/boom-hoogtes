set anaconda3_location=%1

set anaconda3_location="C:\Users\Derek\Anaconda3"


rem fixed parameter
set CONDA_ENV=\envs\conda_trees2

rem create conda env
set conda_polygons_location=%anaconda3_location%%CONDA_ENV%

if exist %conda_polygons_location% (
    echo "Conda environment already exists"
    
    rem update packages
    call conda activate conda_trees2
    call conda update --all -y
    call conda deactivate

) else (
    echo "Conda environment does not yet exist"
    call conda create --name conda_trees2 pandas geopandas rasterio matplotlib descartes shapely openpyxl rasterstats -y
)


call conda activate conda_trees2
python boomhoogtes_from_ahn.py