import xlsxwriter

def printXlsx(station, fileName, path='./pliki_wyjsciowe'):

  outputPath = path+'/'+fileName+'.xlsx'
  workbook = xlsxwriter.Workbook(outputPath)
  worksheet = workbook.add_worksheet()

  bold = workbook.add_format({'bold': True})
  cellFormat = workbook.add_format()
  cellFormat.set_align('center_across')
  cellFormat.set_align('justify')
  bold.set_align('center')

  row = 1
  col = 0
  if type(station) != list:
      stationMethods = {
         'dekodDate': str(station.decodeDate()),
         'miastoPanstwo': str(
         station.decodeCityCountry()['miasto'])
         +'  '+str(
         station.decodeCityCountry()['panstwo']),
         'rodzajStacji': str(
         station.decodeKindOfStation()),
         'typStacji': str(
         station.decodeStationType()),
         'Temp': str(
         station.decodeTemp()),
         'TempPktRos': str(
         station.decodeDewPointTemp()),
         'cisnNaPozMor': str(
         station.decodeSeaLvlPressure()),
         'cisNaPozSt': str(
         station.decodeStationAtmPressure()),
         'wlkZachmOgolnego': str(
         station.decodeCloudGeneral()),
         'wysWzgldnPodstNajnChmr': str(
         station.decodeRelHeightLowClouds()),
         'metPomWiatr': str(
         station.decodeWindIndicator()['metodaPom']),
         'kierunekWiatru': str(
         station.decodeWindDirection()),
         'prdWiatru': str(
         station.decodeWindSpeed()['predkosc'])
         +' '+str(station.decodeWindSpeed()['jednostka']),
         'sumaOpadow': str(
         station.decodePrecipitation()),
         'czasOpadow': str(
         station.decodePrecipitationTimeInHours())
         }
      expList = [stationMethods['dekodDate'], 
         stationMethods['miastoPanstwo'],
         stationMethods['rodzajStacji'], 
         stationMethods['typStacji'],
         stationMethods['Temp'], stationMethods['TempPktRos'],
         stationMethods['cisnNaPozMor'], stationMethods['cisNaPozSt'],
         stationMethods['wlkZachmOgolnego'], 
         stationMethods['wysWzgldnPodstNajnChmr'],
         stationMethods['metPomWiatr'], 
         stationMethods['kierunekWiatru'],
         stationMethods['prdWiatru'], stationMethods['sumaOpadow'],
         stationMethods['czasOpadow']]

      titleList = ['Data','Lokalizacja',
         'Rodzaj stacji','Typ stacji',
         'Temperatura','Temperatura punktu rosy',
         'Cisnienie nad poziomem morza',
         'Cisnienie na poziomie stacji',
         'Wielkosc zachmurzenia ogolnego',
         'Wysokosc wzgledna podstawy najnizszych chmur',
         'Metoda pomiaru wiatru',
         'Kierunek wiatru','Predkosc wiatru',
         'Suma opadow','Czas opadow']
      titleLen = len(titleList)
      for number in range(titleLen):
          worksheet.write(0, col+number, titleList[number], bold)
      expListSizes = []
      titlesSize = []
      for monthy in expList:
          expListSizes.append(len(str(monthy)))
      for monthy in titleList:
          titlesSize.append(len(str(monthy)))

      maksimumWlkTitle = max(titlesSize)
      maksIntTitle = int(maksimumWlkTitle)

      maxExpListSizes = max(expListSizes)
      maksIntExpList = int(maxExpListSizes)
      maksimum = max(maksIntTitle, maksIntExpList)
      sumCells = len(expList)-1
      worksheet.set_column(0, sumCells, maksimum)
      for numer in range(sumCells):
          worksheet.write(row, col+numer, expList[numer], cellFormat)
      workbook.close()

  elif type(station) == list:
      expList = []
      for cell in station:
          cellMethods = { 'dekodDate': str(
            cell.decodeDate()),
            'miastoPanstwo': str(
            cell.decodeCityCountry()['miasto'])
            +'  '+str(
            cell.decodeCityCountry()['panstwo']),
            'rodzajStacji': str(
            cell.decodeKindOfStation()),
            'typStacji': str(
            cell.decodeStationType()),
            'Temp': str(
            cell.decodeTemp()),
            'TempPktRos': str(
            cell.decodeDewPointTemp()),
            'cisnNaPozMor': str(
            cell.decodeSeaLvlPressure()),
            'cisNaPozSt': str(
            cell.decodeStationAtmPressure()),
            'wlkZachmOgolnego': str(
            cell.decodeCloudGeneral()),
            'wysWzgldnPodstNajnChmr': str(
            cell.decodeRelHeightLowClouds()),
            'metPomWiatr': str(
            cell.decodeWindIndicator()['metodaPom']),
            'kierunekWiatru': str(
            cell.decodeWindDirection()),
            'prdWiatru': str(
            cell.decodeWindSpeed()['predkosc'])
            +' '+str(cell.decodeWindSpeed()['jednostka']),
            'sumaOpadow': str(
            cell.decodePrecipitation()),
            'czasOpadow': str(
            cell.decodePrecipitationTimeInHours())
            }

          li = [cellMethods['dekodDate'], 
              cellMethods['miastoPanstwo'],
              cellMethods['rodzajStacji'], 
              cellMethods['typStacji'],
              cellMethods['Temp'], 
              cellMethods['TempPktRos'],
              cellMethods['cisnNaPozMor'], 
              cellMethods['cisNaPozSt'],
              cellMethods['wlkZachmOgolnego'], 
              cellMethods['wysWzgldnPodstNajnChmr'],
              cellMethods['metPomWiatr'], 
              cellMethods['kierunekWiatru'],
              cellMethods['prdWiatru'], 
              cellMethods['sumaOpadow'],
              cellMethods['czasOpadow']]
          expList.append(li)

      expenses = tuple(expList)

      numerSt = 0

      for (dD,mP,rS,tS,temp,tPR,cNPM,
           cNPS,wZO,wWPNC,mPW,kW,pW,sO,
           cO) in (expenses):
          worksheet.write(row, 
              col, numerSt, bold)
          worksheet.write(row, 
              col+1, dD, cellFormat)
          worksheet.write(row, 
              col+2, mP, cellFormat)
          worksheet.write(row, 
              col+3, rS, cellFormat)
          worksheet.write(row, 
              col+4, tS, cellFormat)
          worksheet.write(row, 
              col+5, temp, cellFormat)
          worksheet.write(row, 
              col+6, tPR, cellFormat)
          worksheet.write(row, 
              col+7, cNPM, cellFormat)
          worksheet.write(row, 
              col+8, cNPS, cellFormat)
          worksheet.write(row, 
              col+9, wZO, cellFormat)
          worksheet.write(row, 
              col+10, wWPNC, cellFormat)
          worksheet.write(row, 
              col+11, mPW, cellFormat)
          worksheet.write(row, 
              col+12, kW, cellFormat)
          worksheet.write(row, 
              col+13, pW, cellFormat)
          worksheet.write(row, 
              col+14, sO, cellFormat)
          worksheet.write(row, 
              col+15, cO, cellFormat)
          numerSt += 1
          row += 1
      titleList = ['L.P.','Data','Lokalizacja',
                  'Rodzaj stacji','Typ stacji',
                  'Temperatura','Temperatura punktu rosy',
                  'Cisnienie nad poziomem morza',
                  'Cisnienie na poziomie stacji',
                  'Wielkosc zachmurzenia ogolnego',
                  'Wysokosc wzgledna podstawy najnizszych chmur',
                  'Metoda pomiaru wiatru',
                  'Kierunek wiatru','Predkosc wiatru',
                  'Suma opadow','Czas opadow']
      titleLen = len(titleList)
      col = 0
      for number in range(titleLen):
          worksheet.write(0, col+number, titleList[number], bold)
      stationsSizeList = []
      titlesSize = []
      for monthy in expList:
          for spam in monthy:
              stationsSizeList.append(len(str(spam)))

      maksimum = max(stationsSizeList)
      maksInt = int(maksimum)

      for monthy in titleList:
          titlesSize.append(len(monthy))
      maksTitleSize = max(titlesSize)
      maksTitleInt = int(maksTitleSize)
      if maksInt < maksTitleInt:
          maksInt = maksTitleInt
      worksheet.set_column(0,titleLen, maksInt)
      workbook.close()
