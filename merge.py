import os
import pandas as pd
import csv
from decimal import Decimal

path = "/Users/kylechin/Grace-GraceFo_Scrapper/lwe_data/"
file_type = ".csv"
all_csv = sorted([file_name for file_name in os.listdir(path) if '.csv' in file_name])
final_file = "/Users/kylechin/Grace-GraceFo_Scrapper/final.csv"
# for file in all_csv:
#   print(file.split("_")[1])
with open(final_file, "a") as final:
  writer = csv.writer(final);
  header = ["Coordinate"]
  for file in all_csv:
    with open(path + file, "r") as csv_file:
      csv_reader = csv.reader(csv_file)
      counter = 1
      for row in csv_reader:
        if counter == 2:
          date = row[3].split("(")[1].split(")")[0].split()[0]
          header.append(date)
          # print(date)
          break
        counter += 1
    csv_file.close()
    
  writer.writerow(header)
  all_data = dict();
final.close()

with open(path + all_csv[0], "r") as file:
  csv_reader = csv.reader(file)
  for row in csv_reader:
    if row[0] != "Latitude":
      coord = (float(row[0]), float(row[1]))
      # print(row[0], row[1], row[2])
      all_data[coord] = list()
      all_data[coord].append(Decimal(row[2]))
      # print(coord, all_data[coord])
file.close()

for i in range(1, len(all_csv)):
  with open(path + all_csv[i], "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
      if row[0] != "Latitude":
        coord = (float(row[0]), float(row[1]))
        all_data[coord].append(Decimal(row[2]))
        # print(coord, all_data[coord])
  file.close()
# for i in all_data.keys():
#   print(i, all_data[i])
with open(final_file, "a") as final:
  csv_writer = csv.writer(final)
  counter = 0
  for i in all_data.keys():
    row = all_data[i]
    # print(row)
    if not all(val == 0 for val in row):
      row.insert(0, i)  
      csv_writer.writerow(row)
    
final.close()
      
