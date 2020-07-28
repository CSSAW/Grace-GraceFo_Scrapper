import csv
import os

# all_rows = []
# with open("lwe_data.csv", "r") as csv_file:
#   reader = csv.reader(csv_file)

#   counter = 1
#   for row in reader:
#     # print(row)
#     if counter == 1:
#       rowx = row
#       for i in range(1, len(rowx)):
#         date = rowx[i]
#         date = date.split("/")
#         yyyy = "20" + date[2]
#         if len(date[0]) == 1:
#           date[0] = "0" + date[0]
#         mm = date[0]
#         if len(date[1]) == 1:
#           date[1] = "0" + date[1]
#         dd = date[1]
#         date = [yyyy, mm, dd]
#         rowx[i] = "".join(date)
#       all_rows.append(rowx)
#     else:
#       all_rows.append(row)
#     counter+=1
# csv_file.close()
# # print(all_rows[1])


# with open("all_data.csv", "w") as csv_file:
#   writer = csv.writer(csv_file)
#   for row in all_rows:
#     writer.writerow(row)
# csv_file.close()

directory = os.getcwd()
# print(directory)
grace_data = directory + "/grace_data"
gracefo_data = directory + "/gracefo_data"
# print(grace_data, gracefo_data)
grace_csv = sorted([file_name for file_name in os.listdir(grace_data)])
gracefo_csv = sorted([file_name for file_name in os.listdir(gracefo_data)])
# print(grace_csv)
# print(gracefo_csv)

final_file = directory + "/unmerged_lwe.csv"

with open(final_file, "w") as final_csv:
  csv_writer = csv.writer(final_csv)
  # write in header
  csv_writer.writerow(["Latitude", "Longitude", "LWE_Data", "Date"])
  # traverse all csv files for grace
  for file in grace_csv:
    # open each one and read
    with open(grace_data +'/'+ file, "r") as current_csv:
      csv_reader = csv.reader(current_csv)
      counter = 1
      # loop through all rows except for the header row
      for row in csv_reader:
        if counter != 1:
          # print(row)
          # parse the date to form YYYYMMDD
          row[3] = row[3].split("-")
          row[3] = "".join(row[3])
          # eliminate rows with null data
          if row[2] != "--":
            # print(row)
            csv_writer.writerow(row)
        counter += 1 
    current_csv.close()
        
  for file in gracefo_csv:
    with open(gracefo_data+ "/" +file, "r") as current_csv:
      csv_reader = csv.reader(current_csv)
      counter = 1
      for row in csv_reader:
        if counter != 1:
          # parse the date to form YYYYMMDD
          row[3] = row[3].split(" ")
          row[3] = row[3][0].split("(")[1]
          row[3] = "".join(row[3].split("-"))
          # eliminate rows with null data
          if row[2] != "0.00000":
            csv_writer.writerow(row)
        counter += 1
    current_csv.close()
final_csv.close()