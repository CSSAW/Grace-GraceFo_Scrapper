import podaac.podaac as podaac
import podaac.podaac_utils as utils
import podaac.drive as pd


p = podaac.Podaac()
u = utils.PodaacUtils()
# drive = pd.Drive("jpl_data.txt", "qinz", "1y@0g8BKgJUkTBCq@9N", "https://podaac-tools.jpl.nasa.gov/drive/files/allData/tellus/L3/gracefo/land_mass/RL06/v03/JPL")

data_var = p.dataset_variables(dataset_id='PODAAC-GFLND-3AJ63')
# print(data_var)

granules = p.granule_search(dataset_id='PODAAC-GFLND-3AJ63', bbox='16.3335213, -47.1788335,38.2898954,-22.1230301', _format="html")
# granules = p.granule_search(dataset_id='PODAAC-GFLND-3AJ63', _format="html")
# print(granules)
drive = pd.Drive(file="/Users/kylechin/Desktop/haha.txt", username="qinz", password="1y@0g8BKgJUkTBCq@9N", webdav_url="https://podaac.jpl.nasa.gov/dataset/TELLUS_GRFO_L3_JPL_RL06_LND_v03")
# drive2 = pd.Drive()