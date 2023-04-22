import scraper as s

dir = s.Directory()
 
print(dir.brandsMap)
for brand in dir.brands:
    print(brand.table)