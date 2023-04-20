# first web scraper
# supposed to scrape tennis stringing data from klippermate website

import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

class Brand:
    # creates table with racquet name as key, and list of all values
    allowedBrands = {
        "babolat":"https://klipperusa.com/pages/babolat-tennis-racquet-patterns",
        "wilson":"https://klipperusa.com/pages/wilson-tennis-racquet-patterns",
        "head":"https://klipperusa.com/pages/head-tennis-racquet-patterns",
        "yonex":"https://klipperusa.com/pages/yonex-tennis-racquet-patterns"
        }

    def __init__(self, brand):
        self.brand = brand
        self.table = self.createTable(self.brand)
    
    def createTable(self, brand):
        page = requests.get(Brand.allowedBrands[brand])
        soup = BeautifulSoup(page.content, 'html.parser') 

        tb = {}
        rows = soup.select("table tbody tr") 
        for row in rows:
            td_list = row.find_all("td")
            for i in range(len(td_list)):
                td_list[i] = td_list[i].string 
            if len(td_list) != 8: continue
            tb.update({td_list[0]:td_list[1:]})
        
        return tb

    def getListOfModels(self, query):
        default = self.table.keys()
        if not query: return default
        new = []
        # do some algorithm stuff with query to eliminate
        # some choices
        # TODO
        for model in default:
            if fuzz.token_set_ratio(query.lower(), model.lower()) > 75:
                new.append(model)
        return new
    
    def getSpecs(self, model):
        return self.table[model]

babolat = Brand("head")
query = "touch speed"
print(babolat.getListOfModels(query))
for model in babolat.getListOfModels(query):
    print(babolat.getSpecs(model))