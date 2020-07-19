import os
import pandas as pd
import csv
from decimal import Decimal

def mergeCSV(path, file_type=".csv", final_filename="test.csv"):
  
  # sort all csv files under this directory by ascending date order
  all_csv = sorted([file_name for file_name in os.listdir(path) if file_type in file_name])
  final_file = os.getcwd() + final_filename + file_type
  # print(all_csv)

  # write the header bar by collecting time from all files to be merged
  with open(final_file, "a") as final:
    writer = csv.writer(final);
    header = ["Coordinate"]
    for file in all_csv:
      with open(path + file, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        counter = 1
        for row in csv_reader:
          if counter == 2:
            date = row[3]
            header.append(date)
            # print(date)
            break
          counter += 1
      csv_file.close()
    writer.writerow(header)
  final.close()

  # Use dictionary with Coordiante tuples as keys, and a list of lwe data as correspoonding values
  all_data = dict();

  # use the first file in directory to initialize the dictionary, it'll eventually be there why not now
  with open(path + all_csv[0], "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
      if row[0] != "Latitude":
        coord = (float(row[0]), float(row[1]))
        # print(row[0], row[1], row[2])
        all_data[coord] = list()
        if (row[2] == "--"):
          all_data[coord].append(0)
        else: 
          all_data[coord].append(Decimal(row[2]))
        # print(coord, all_data[coord])
  file.close()

  # keep doing it
  for i in range(1, len(all_csv)):
    with open(path + all_csv[i], "r") as file:
      csv_reader = csv.reader(file)
      for row in csv_reader:
        if row[0] != "Latitude":
          coord = (float(row[0]), float(row[1]))
          if (row[2] == "--"):
            all_data[coord].append(0)
          else: 
            all_data[coord].append(Decimal(row[2]))
          # print(coord, all_data[coord])
    file.close()

  # for i in all_data.keys():
  #   print(i, all_data[i])

  # The final csv file containing Coordinate, Time as the header bar, coordinates in tuples under Coordinate, and land water equivalence data below Time.
  with open(final_file, "a") as final:
    csv_writer = csv.writer(final)
    counter = 0
    for i in all_data.keys():
      row = all_data[i]
      # print(row)
      # If all the elements of current corrdinate are not defined float, ignore them.
      if not all(val == 0 for val in row):
        row.insert(0, i)  
        csv_writer.writerow(row)
      
  final.close()

if __name__ == "__main__":

  grace_path = os.getcwd() + "/grace_lwe_data/"
  gracefo_path = os.getcwd() + "/gracefo_lwe_data/"
  file_type = ".csv"
  grace_filename = "/grace_lwe_data"
  gracefo_filename = "/gracefo_lwe_data"
  # mergeCSV(grace_path, file_type, grace_filename)
  mergeCSV(gracefo_path, file_type, gracefo_filename)
      
