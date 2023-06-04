from .context import tennis_scraper

dir = tennis_scraper.scraper.Directory()
 
print(dir.brandsMap)
for brand in dir.brands:
    print(brand.table)
