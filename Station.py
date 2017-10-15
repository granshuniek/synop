from cities import openCounCity,groupCities,getCountCity
class Station(dict):
    '''Klasa tworzaca obiekty stacji
    meteorologicznych oraz przechowujaca
    konkretne wartosci depeszy SYNOP, a takze
    je dekodujaca. Do klasy podajemy pojedyncza depesze, a nie liste depesz.
    Argumenty:
        getSynopType:
            - 'file' jezeli depesza podana z pliku
            - 'web' jezeli depesza pobrana z sieci
            synopCode:
                tekst depeszy z pliku lub sieci
    '''

    def __init__(self,  getSynopType, synopCode):
        dict.__init__(self)

        # elementy obligatoryjne (mandatory elements)

        if getSynopType == 'file':
            indx = 0
            synopCode = synopCode.split()
            synopCodeMand = synopCode[:6]
            synopCodeOptional = synopCode[6:]
            element0 = synopCodeMand[indx]
            self['godzinaUTC'] = element0[8:10]             
            self['minutaUTC'] = element0[10:]              
            self['rok'] = element0[:4]                      
            self['miesiac'] = element0[4:6]                 
            self['dzien'] = element0[6:8]                   

        elif getSynopType == 'web':
            indx = 5
            synopCodeMand = synopCode[:11]
            synopCodeOptional = synopCode[11:]
            self['godzinaUTC'] = synopCodeMand[4]             
            self['minutaUTC'] = synopCodeMand[5]               
            self['rok'] = synopCodeMand[1]                     
            self['miesiac'] = synopCodeMand[2]                 
            self['dzien'] = synopCodeMand[3] 


        #element 1
        element1 = synopCodeMand[indx+1]
        self['rodzajStacji'] = element1
        #element 2
        element2 = synopCodeMand[indx+2]
        self['dzienMies'] = element2[:2]
        self['godzinaObs'] = element2[2:4]
        self['wskWiatru'] = element2[4]
        #element 3
        element3 = synopCodeMand[indx+3]
        self['kraj'] = element3[:2]
        self['miasto'] = element3[2:]
        #element 4
        element4 = synopCodeMand[indx+4]
        self['grupaOpad'] = element4[0]
        self['typ'] = element4[1]
        self['wysWzgldnPodstNajnChmr'] = element4[2]
        self['widzPozioma'] = element4[3:]
        #element 5
        element5 = synopCodeMand[indx+5]
        self['wlkZachmOgol'] = element5[0]
        self['kierWiatrWSt'] = element5[1:3]
        self['prdWiatrWJedn'] = element5[3:]  

        # elementy fakultatywne (optional elements)
        groupDict = {}
        for cell in synopCodeOptional:
            groupDict[cell[0]] = cell

        for key in groupDict:
            if key == '1':
                element1 = groupDict[key]
                self['ozGr1'] = element1[0]
                self['znakTemp'] = element1[1]
                self['wartTempWDecStrCel'] = element1[2:]
            if key == '2':
                element2 = groupDict[key]
                self['ozGr2'] = element2[0]
                self['znakTempPktRos'] = element2[1]
                self['tempPktRos'] = element2[2:]
            if key == '3':
                element3 = groupDict[key]
                self['ozGr3'] = element3[0]
                self['cisnNaPozSt'] = element3[1:]
            if key == '4':
                element4 = groupDict[key]
                self['ozGr4'] = element4[0]
                self['cisNaPozMorza'] = element4[1:]
            if key == '5':
                element5 = groupDict[key]
                self['ozGr5'] = element5[0]
                self['tendCisn'] = element5[1]
                self['wlkTend'] = element5[2:]
            if key == '6':
                element6 = groupDict[key]
                self['ozGr6'] = element6[0]
                self['sumPrecipitationow'] = element6[1:4]
                self['czasOpad'] = element6[4]
            if key == '7':
                element7 = groupDict[key]
                self['ozGr7'] = element7[0]
                self['pogBiez'] = element7[1:3]
                self['pogPoprz'] = element7[3:]
            if key == '8':
                element8 = groupDict[key]
                self['ozGr8'] = element8[0]
                self['zachPrzezChmNisk'] = element8[1]
                self['rodzajeChmur'] = element8[2:]


    #metody dekodujace

    #metody dekodujace elementy obligatoryjne

    def decodeDate(self):
        day = self['dzien']
        month = self['miesiac']
        year = self['rok']
        hour = self['godzinaUTC']
        minute = self['minutaUTC']
        date = (day + '/' + month 
                + '/' + year + '   ' 
                + hour + ':' + minute)
        return date

    def decodeKindOfStation(self):
        '''Dekoduje rodzaj stacji, 
        tj. czy stacja na 
        ktorej dokonano obserwacji
        jest stacja ladowa,
            statkiem czy boja'''
        kindCode = self['rodzajStacji']
        if kindCode == "AAXX":
            rep = "stajca ladowa"
        elif kindCode == "BBXX":
            rep = "statek"
        else:
            rep = "boja"
        return rep

    def decodeWindIndicator(self):
        '''Dekoduje wskaznik wiatru. 
            Ten przechowuje informacje o 
            metodzie pomiaru predkosci
           wiatru oraz jednostkach w jakich 
           zostala dokonana obserwacja'''
        windIndCode = self['wskWiatru']
        if windIndCode == '0':
            windInd = {"jednostka":"m/s", 
            "metodaPom":"wiatromierz Wilda lub szacowana"}
        elif windIndCode == '1':
            windInd = {"jednostka":"m/s", 
                        "metodaPom":"anemometr"}
        elif windIndCode == '3':
            windInd = {"jednostka":"wezly", 
            "metodaPom":"wiatromierz Wilda lub szacowana"}
        elif windIndCode == '4':
            windInd = {"jednostka":"wezly", 
            "metodaPom":"anemometr"}
        return windInd

    def decodeCityCountry(self):
        '''Dekoduje miasto, z ktorego pochodzi depesza'''
        citiesList = groupCities(
            openCounCity('./dane/polska_stacje.txt'))
        rep = getCountCity(citiesList, self['miasto'])
        return rep

    def decodeStationType(self):
        '''Dekoduje typ stacji, 
            tj. czy stacja dokonuje 
            obserwacji automatycznie, 
            czy za pomoca czlowieka'''
        stationTypeCode = str(self['typ'])
        if (stationTypeCode == '1' 
            or stationTypeCode == '2' 
            or stationTypeCode == '3'):
            rep = 'nieautomatyczna'
        elif (stationTypeCode == '4' 
            or stationTypeCode == '5' 
            or stationTypeCode == '6' 
            or stationTypeCode == '7'):
            rep = 'automatyczna'
        else:
            rep = 'Brak danych'
        return rep

    def decodeRelHeightLowClouds(self):
        '''Dekoduje wysokosc wzgledna najnizszych chmur.'''
        hCloudsCode = self['wysWzgldnPodstNajnChmr']
        if hCloudsCode == '0':
            rep = '0-59'
        elif hCloudsCode == '1':
            rep = '50-100'
        elif hCloudsCode == '2':
            rep = '100-200'
        elif hCloudsCode == '3':
            rep = '200-300'
        elif hCloudsCode == '4':
            rep = '300-600'
        elif hCloudsCode == '5':
            rep = '600-1000'
        elif hCloudsCode == '6':
            rep = '1000-1500'
        elif hCloudsCode == '7':
            rep = '1500-2000'
        elif hCloudsCode == '8':
            rep = '2000-2500'
        elif hCloudsCode == '9':
            rep = '>2500'
        else:
            rep = 'Brak danych'
        return rep

    def decodeCloudGeneral(self):
        '''Dekoduje wielkosc zachmurzenia ogolnego'''
        cloudCode = self['wlkZachmOgol']
        rep = str(cloudCode)+'/8'
        if cloudCode == '/':
            rep = 'Brak danych'
        return rep

    def decodeWindDirection(self):
        '''Dekoduje kierunek wiatru'''
        try:
            directionCode = self['kierWiatrWSt']
            directionCodeInt = int(directionCode)
            if directionCode == '00':
                rep = 'cisza'
            elif directionCode == '36':
                rep = '355-4'
            elif directionCode == '99':
                rep = 'zmienny'
            elif directionCodeInt >= 1 and directionCodeInt < 36:
                iloscDziesiatek = directionCodeInt*10
                minWindDirection = 5+(iloscDziesiatek-10)
                maxWindDirection = minWindDirection+10-1
                rep = str(minWindDirection)+'-'+str(maxWindDirection)
        except ValueError:
            rep = 'Brak obserwacji'
        return rep

    def decodeWindSpeed(self):
        '''Dekoduje predkosc wiatru.'''
        try:
            windInd = self.decodeWindIndicator()
            mesUnit = windInd['jednostka']
            spWind = self['prdWiatrWJedn']
            spWindRep = float(spWind)
        except ValueError:
            spWindRep = "Brak danych"
        rep = { 'predkosc': spWindRep, 'jednostka': mesUnit}
        return rep

    #metody dekodujace elementy fakultatywne

    def decodeTemp(self):
        '''Dekoduje temperature w stopniach Celsjusza'''
        try:
            tempCode = self['wartTempWDecStrCel']
            varTempCode = self['znakTemp']
            rep = float(tempCode)
            if str(varTempCode) == '1':
                rep = -1*rep
            rep /= 10
        except KeyError,ValueError:
            rep = 'Brak danych'
        return rep

    def decodeDewPointTemp(self):
        '''Dekoduje temperature punktu rosy w stopniach Celsjusza'''
        try:
            dPTempCode = self['tempPktRos']
            varDPTempCode = self['znakTempPktRos']
            rep = float(dPTempCode)
            if str(varDPTempCode) == '1':
                rep = -1*rep
            rep /= 10
        except KeyError,ValueError:
            rep = 'Brak danych'
        return rep

    def decodeStationAtmPressure(self):
        '''Dekoduje cisnienie na poziomie stacji w hPa'''
        try:
            presCode = self['cisnNaPozSt']
            presFloat = float(presCode)
            if presCode[0] == '0':
                presFloat += 10000
            presFloat *= 0.1
            return presFloat
        except KeyError,ValueError:
            return 'Brak danych'

    def decodeSeaLvlPressure(self):
        '''Dekoduje cisnienie 
        zrownane do poziomu morza (jedynie stacje
        lezace nie wyzej niz 500 m n.p.m.)'''
        try:
            seaPressCode = self['cisNaPozMorza']
            seaPressFloat = float(seaPressCode)
            if (self['miasto'] == '625' 
                or self['miasto'] == '650' 
                or self['miasto'] == '510'):
                return 'Zabronione'
            else:
                if seaPressCode[0] == '0':
                    seaPressFloat += 10000
                seaPressFloat *= 0.1
                return seaPressFloat
        except KeyError,ValueError:
            return 'Brak danych'

    def decodePrecipitationTimeInHours(self):
        try:
            timeCode = self['czasOpad']
            timeCodeInt = int(timeCode)
            baseFirst = 6
            baseSecond = 4
            if timeCode == '/':
                return '24'
            elif timeCodeInt < 5:
                rep = str(baseFirst*timeCodeInt)
            elif 5 <= timeCodeInt < 8:
                rep = str(timeCodeInt - baseSecond)
            elif timeCode == '8':
                rep = '9'
            elif timeCode == '9':
                rep = '15'
            return rep
        except KeyError,ValueError:
            return 'Brak danych'

    def decodePrecipitation(self):
        '''Dekoduje sume opadow'''
        try:
            sumPrecipitationCode = self['sumaOpadow']
            base = sumPrecipitationCode[:2]
            slad = sumPrecipitationCode[:3]
            if base != '99':
                sumPrecipitationFloat = float(
                    sumPrecipitationCode)
                return sumPrecipitationFloat
            elif base == '99' and slad != '990':
                sumPrecipitationFloat = float(
                    sumPrecipitationCode[2])*0.1
                return sumPrecipitationFloat
            elif sumPrecipitationCode == '990':
                sumPrecipitationFloat = 'slad'
            elif sumPrecipitationCode == '000':
                return 'Brak opadow'
        except KeyError,ValueError:
            return 'Brak danych'