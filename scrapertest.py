import scraper as s

babolat = s.Brand("babolat")
query = "pure aero"
print('query:',query)
print(babolat.getListOfModels(query))
for model in babolat.getListOfModels(query):
    print(babolat.getSpecs(model))

head = s.Brand("head")
query = "touch speed"
print('query:',query)
print(head.getListOfModels(query))
for model in head.getListOfModels(query):
    print(model,':',head.getSpecs(model))