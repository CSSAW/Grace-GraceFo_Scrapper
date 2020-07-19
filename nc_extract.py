import numpy as np
import netCDF4 as nc
import pandas as pd
import csv
import os

# Reads netCDF file from specified path and extract data within the coordinate bounding box
def readNC(file_path, lat_max, lat_min, lon_max, lon_min):

	current_dir = os.getcwd() + "/grace_lwe_data/"
	file = nc.Dataset(file_path, mode="r")
	source_name = file_path.split(".")[0].split("/")
	source_name = source_name[len(source_name)-1]
	print(source_name)
	
	print("File being processed is " + file_path)
	for i in file.variables.keys():
		print(i, end='\t')
	print()
	print(lat_max, lat_min, lon_max, lon_min)
	lat = file.variables["lat"]
	lon = file.variables["lon"]
	lwe = file.variables["lwe_thickness"]
	time = file.variables["time"]
	dtime = nc.num2date(time[:], time.units)
	dtime = str(dtime).split("(")[1].split(")")[0].split()[0]
	print(file["lwe_thickness"].dimensions)
	with open(source_name.split("_")[1] + ".csv", "a", newline="") as target:
		writer = csv.writer(target)
		writer.writerow(("Latitude", "Longitude", "LWE"))
		for i in range(len(lat)):
			for j in range(len(lon)):
				# print(lat[i], lon[j])
				if (lat[i] > lat_max and lat[i] < lat_min and lon[j] < lon_max and lon[j] > lon_min):
					writer.writerow(("{:.2f}".format(lat[i]), "{:.2f}".format(lon[j]), "{:.5f}".format(lwe[0][i][j]), dtime))
					# print((lat[i], lon[j]))
		
	target.close()
	file.close()
	

	

if __name__ == "__main__":
    
	
	file_path = os.getcwd() + "/allData/tellus/L3/gracefo/land_mass/RL06/v03/JPL/GRD-3_2018152-2018181_GRFO_JPLEM_BA01_0600_LND_v03.nc"
	# South African latitude and longitude bounding box
	lat_max, lat_min, lon_max, lon_min = -47, -22, 38.5, 16.5
	readNC(file_path, lat_max, lat_min, lon_max, lon_min)

