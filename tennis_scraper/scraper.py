# first web scraper
# scrapes tennis stringing data from klippermate website

import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

"""
Data structure representing the directory of racquet brands

self.brandsMap - map with brandname as key and database url as value
self.brands - list of Brand data structures
"""


class Directory:
    dirURL = "https://klipperusa.com/pages/racquet-stringing-patterns"
    brandsMap = {}
    brands = []

    def __init__(self):
        self.scrapeDir()
        self.scrapeSubDirs()

    # constructs brandsMap
    def scrapeDir(self):
        page = requests.get(self.dirURL)
        soup = BeautifulSoup(page.content, 'html.parser')

        links = soup.select("table tbody tr td ul li a")
        url = 'https://klipperusa.com'
        for link in links:
            if "tennis" in link.text.lower():
                self.brandsMap[link.text] = url+str(link.get('href'))

    # constructs brands
    def scrapeSubDirs(self):
        for brandName in self.brandsMap:
            brand = Brand(brandName, self.brandsMap)
            self.brands.append(brand)


"""
Data Structure representing each racquet brand

self.brand - brand name
self.table - table with model as key and list of specs as value
"""


class Brand:
    # creates table with racquet name as key, and list of all values
    def __init__(self, brand, brandsMap):
        self.brand = brand
        self.table = self.createTable(brand, brandsMap)

    # Constructs data structure using web scraping
    def createTable(self, brand, brandsMap):
        page = requests.get(brandsMap[brand])
        soup = BeautifulSoup(page.content, 'html.parser')

        tb = {}
        rows = soup.select("table tbody tr")
        for row in rows:
            td_list = row.find_all("td")
            for i in range(len(td_list)):
                td_list[i] = td_list[i].string
            if len(td_list) != 8:
                continue
            tb.update({td_list[0]: td_list[1:]})
        return tb

    # Return all models for brand which "match" the query
    def getListOfModels(self, query):
        default = self.table.keys()
        if not query:
            return default
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

    # Returns specs for a given model
    def getSpecs(self, model):
        return self.table[model]
