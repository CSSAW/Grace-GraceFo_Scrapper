import podaac.podaac as podaac
import podaac.podaac_utils as utils
import podaac.drive as pd


p = podaac.Podaac()
u = utils.PodaacUtils()
drive = pd.Drive(file="podaac.ini", username="qinz", password="1y@0g8BKgJUkTBCq@9N", webdav_url="https://podaac-tools.jpl.nasa.gov/drive/files")

data_var = p.dataset_variables(dataset_id='PODAAC-GFLND-3AJ63')
print(data_var)

# # granules = p.granule_search(dataset_id='PODAAC-GFLND-3AJ63', bbox='16.3335213, -47.1788335,38.2898954,-22.1230301', _format="html")
granules = p.granule_search(dataset_id='PODAAC-GFLND-3AJ63')
# print(granules)

results = drive.mine_drive_urls_from_granule_search(granule_search_response=granules)
print(results)

drive.download_granules(results, path="/Users/kylechin/Grace-GraceFo_Scrapper")

