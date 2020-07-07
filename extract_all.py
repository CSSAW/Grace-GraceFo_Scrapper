from nc_extract import readNC
import os

current_path = os.getcwd()
print(current_path)
nc_files = []
path = "/Users/kylechin/Grace-GraceFo_Scrapper/allData/tellus/L3/gracefo/land_mass/RL06/v03/JPL"
lat_max, lat_min, lon_max, lon_min = -47, -22, 38.5, 16.5
for i in os.listdir(path):
  if os.path.splitext(i)[1] == ".nc":
    print(os.path.splitext(i)[0])
    this_path = path + "/" + i
    readNC(this_path, lat_max, lat_min, lon_max, lon_min)

print("All netCDF files data are extracted.")



