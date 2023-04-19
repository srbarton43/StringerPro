# first web scraper
# supposed to scrape tennis stringing data from klippermate website

import requests
from bs4 import BeautifulSoup

fp = open("babolat.html")
soup = BeautifulSoup(fp, 'html.parser') 


# creates table with racquet name as key, and list of all values
table = {}
rows = soup.select("table tbody tr") 
print(rows)    
for row in rows:
    td_list = row.find_all("td")
    for i in range(len(td_list)):
       td_list[i] = td_list[i].string 

    if len(td_list) != 8: continue
    table.update({td_list[0]:td_list[1:]})

print(table)
