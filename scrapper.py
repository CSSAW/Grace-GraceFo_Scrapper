import requests
from bs4 import BeautifulSoup

URL = "https://podaac-tools.jpl.nasa.gov/drive/files/allData/tellus/L3/gracefo/land_mass/RL06/v03/JPL"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
content = soup.find(id="podaac-page-content")
print(content)