from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

#token = urlopen("https://www.upwork.com/")
token1 = requests.Request("https://www.upwork.com/", headers={'User-Agent': 'Mozilla/5.0'})
bsobj = BeautifulSoup(token1, "html.parser")

findme = bsobj.find("li", {"class": "d-none d-lg-block nav-dropdown", "data-cy": "menu"})
x = findme.find("button", {"class": "nav-item"})
z = x.find("span", {"class": "nav-item-label"})

print(z.get_text())