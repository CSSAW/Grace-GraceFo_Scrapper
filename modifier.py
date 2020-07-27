import csv

all_rows = []
with open("lwe_data.csv", "r") as csv_file:
  reader = csv.reader(csv_file)

  counter = 1
  for row in reader:
    # print(row)
    if counter == 1:
      rowx = row
      for i in range(1, len(rowx)):
        date = rowx[i]
        date = date.split("/")
        yyyy = "20" + date[2]
        if len(date[0]) == 1:
          date[0] = "0" + date[0]
        mm = date[0]
        if len(date[1]) == 1:
          date[1] = "0" + date[1]
        dd = date[1]
        date = [yyyy, mm]
        rowx[i] = "-".join(date)
      all_rows.append(rowx)
    else:
      all_rows.append(row)
    counter+=1
csv_file.close()
# print(all_rows[1])


with open("all_data.csv", "w") as csv_file:
  writer = csv.writer(csv_file)
  for row in all_rows:
    writer.writerow(row)
csv_file.close()