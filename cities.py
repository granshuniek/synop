'''Skrypt sluzy do tworzenia listy miast dla danego kraju (aktualnie jedynie Polska)'''

def openCounCity(path):
    synopFile = open(path)
    read = synopFile.read()
    cityList = read.replace('\n','')
    cityList = str(cityList).replace(' ','')
    synopFile.close()
    cityList = str(cityList).split('#')
    return cityList

def groupCities(cityList):
    counter = 0
    for row in cityList:
        cityList[counter] = str(row).split('|')
        counter += 1
    return cityList

def getCountCity(cityList, cityNumber):
    counter = 0
    for row in cityList:
        if str(cityNumber) == str(row[0][2:]):
            location = {'panstwo': row[2], 'miasto': row[1]}
            counter += 1
            break
    if counter != 1:
        location = {'panstwo': 'brak', 'miasto': 'brak'}
        print 'Brak obiektu w bazie!'
    return location
