# first web scraper
# supposed to scrape tennis stringing data from klippermate website

import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

class Directory:
    dirURL = "https://klipperusa.com/pages/racquet-stringing-patterns"
    brandsMap = {}
    brands = []
    def __init__(self):
        self.scrapeDir()
        self.scrapeSubDirs()

    def scrapeDir(self):
        page = requests.get(self.dirURL)
        soup = BeautifulSoup(page.content, 'html.parser')

        links = soup.select("table tbody tr td ul li a")
        url = 'https://klipperusa.com'
        for link in links:
            if "tennis" in link.text.lower():
                self.brandsMap[link.text] = url+link.get('href')

    def scrapeSubDirs(self):
        for brandName in self.brandsMap:
            brand = Brand(brandName,self.brandsMap)
            self.brands.append(brand)
       



class Brand:
    # creates table with racquet name as key, and list of all values
    def __init__(self, brand, brandsMap):
        self.brand = brand
        self.table = self.createTable(brand,brandsMap)
        
    
    def createTable(self, brand, brandsMap):
        page = requests.get(brandsMap[brand])
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
        for model in default:
            if (
                fuzz.token_set_ratio(query.lower(), model.lower()) > 75
                or query.lower() in model.lower()
            ):
                new.append(model)
        return new
    
    def getSpecs(self, model):
        return self.table[model]
