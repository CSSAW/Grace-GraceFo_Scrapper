import podaac.podaac as podaac
import podaac.podaac_utils as p_utils
import podaac.drive as pd
import os

# Uses NASA's PODAAC drive API to search and download dataset granules into specified local folder

def granule_Download(data_id):

  p = podaac.Podaac()
  u = p_utils.PodaacUtils()
  # Authentication of podaac drive access, if you have installed Podaac API, navigate to its folder and 
  # specify your log in credentials in podaac.ini file.
  drive = pd.Drive(username = "", password="", file="podaac.ini", webdav_url="https://podaac-tools.jpl.nasa.gov/drive/files")


  # data_var = p.dataset_variables(dataset_id = data_id)
  try:
    if data_id == "PODAAC-TELND-3AJ63":
      granule = p.granule_search(dataset_id = data_id)
      print(granule)
    else:
      granule = p.granule_search(dataset_id = data_id)
    print("Dataset with id: {} found".format(data_id))
  except:
    print("Dataset with id: {} not found".format(data_id))

  all_results = drive.mine_drive_urls_from_granule_search(granule_search_response = granule)
  results = []
  local_path = os.getcwd()
  # print(results)

  # Include only nc files in results list
  for url in all_results:
    if (url.split(".")[-1] == "nc"):
      results.append(url)
      # print(url)

  # drive.download_granules(results, path= local_path)

if __name__ == "__main__":

  grace_data_id = "PODAAC-TELND-3AJ63"
  grace_fo_data_id = "PODAAC-GFLND-3AJ63"

  granule_Download(grace_data_id)
  # granule_Download(grace_fo_data_id)

# # GRACE 
# data_var = p.dataset_variables(dataset_id='PODAAC-TELND-3AJ63')


# # GraceFO
# data_var = p.dataset_variables(dataset_id='PODAAC-GFLND-3AJ63')


