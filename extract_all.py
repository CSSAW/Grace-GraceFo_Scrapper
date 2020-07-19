from nc_extract import readNC
import os

def extractAll(datafile_path):

  current_path = os.getcwd()
  print(current_path)
  nc_files = []
  path = current_path + datafile_path

  lat_max, lat_min, lon_max, lon_min = -47, -22, 38.5, 16.5
  for file in os.listdir(path):
    if os.path.splitext(file)[1] == ".nc":
      print(os.path.splitext(file)[0])
      this_path = path + "/" + file
      readNC(this_path, lat_max, lat_min, lon_max, lon_min)

  print("All data in netCDF files under {} are extracted.".format(path))


if __name__ == "__main__":
  gracefo = "/allData/tellus/L3/gracefo/land_mass/RL06/v03/JPL"
  grace = "/allData/tellus/L3/grace/land_mass/RL06/v03/JPL"
  extractAll(grace)


