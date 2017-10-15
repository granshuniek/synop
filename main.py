import Station as St
import getSynop as gS
import printXlsxReport as pXR
import printChart as pC
import datetime as dT
import urllib2 as ur2

def greeting():
    print "Witaj w programie wizualizujacym depesze SYNOP."

def appInfo():
    print ("Program stworzony na "+
    "potrzeby pracy licencjackiej.")
    print ("Temat pracy:        "+
    "\"Wizualizacja w Pythonie"+
    " danych pochodzacych z depeszy SYNOP\"")
    print ("ANG:                 "+
    "\"Visualization of meteorological "+
    "data from SYNOP reports in Python\"")
    print ("Promotor:            "+
    "dr Jaroslaw Bylina")
    print ("Autor:               "+
    "Damian Wiktor Korzeniowski")
    print ("Jednostka naukowa:   "+
    "Uniwersytet Marii Curie Sklodowskiej w Lublinie")
    print ("                         "+
    "Wydzial Matematyki, Fizyki i Informatyki\n")

def checkDate(stationList):
    dateList = []
    for spam in stationList:
        station = St.Station(getSynopType='file', depesza=spam)
        dateList.append(station.decodeDate())
    sumListLen = 0
    listLen = len(stationList)+1
    for eggs in range(listLen):
        if eggs == dateList[eggs]:
            sumListLen +=1
    if sumListLen == listLen:
        return True
    else:
        return False

def daysInMonth(month, year):
    if month == '02':
        if isLeapYear(year):
            numOfDays = 29
        else:
            numOfDays = 28
    else:
        if month == '07' or (float(month) % 7 ) % 2 == 1:
            numOfDays = 31
        else:
            numOfDays = 30
    return numOfDays

def isLeapYear(year):
    year = float(year)
    return ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0)

def isDateCorrect(day, month, year, hour):
    now = dT.datetime.now()
    yearInt = int(year)
    monthInt = int(month)
    dayInt = int(day)
    hourInt = int(hour)
    if yearInt == int(now.year):
        if 1 <= monthInt <= int(now.month):
            if monthInt == int(now.month):
                if 1 <= dayInt <= int(now.day):
                    if dayInt == int(now.day):
                        if 00 <= hourInt <= int(now.hour):
                            return True
                        else:
                            return False
                    else:
                        return (dayInt >= 1 and 
                        dayInt <= daysInMonth(month=month, 
                            year=year) 
                        and 0 <= hourInt and hourInt < 24)
                else:
                    return False
            else:
                return (1 <= monthInt <= 12 and 
                1 <= dayInt <= daysInMonth(month=month,
                    year=year) 
                and 0 <= hourInt < 24)
        else:
            return False
    else:
        return (yearInt > 2000 and monthInt >= 1 
        and monthInt <= 12 and dayInt >= 1 
        and dayInt <= daysInMonth(month=month, year=year) 
        and 0 <= hourInt and hourInt < 24)

def getObservationDateFromUser():
    try:
        print 'Podaj rok YYYY: '
        year = str(raw_input())
        print 'Podaj miesiac MM: '
        month = str(raw_input())
        print 'Podaj dzien DD: '
        day = str(raw_input())
        print 'Podaj godzine HH: '
        hour = str(raw_input())
        cor = isDateCorrect(year=year,month=month,
                            day=day,hour=hour)
        if cor == True:
            repDate = year+month+day+hour+'00'
            return True,repDate
        else:
            repDate = 'Brak'
            return False,repDate
    except NameError:
        repDate = 'Brak'
        print 'Blednie wprowadzono date'
        return False,repDate

def choice(firstNote, amountOfSel, errorAlert):
    amountOfSelections = amountOfSel+1
    print firstNote
    try:
        choice = input()
        for number in range(1, amountOfSelections):
            if choice == number:
                answer = True,choice
                break
            else:
                answer = False,errorAlert
    except NameError:
        answer = False,errorAlert
        # w razie jakby zamiast liczby podano stringa
    except SyntaxError:
        answer = False,errorAlert
    return answer

def zeroReact():
    zChoice = zeroChoice()
    if zChoice == 1:
        appInfo()
        return 'end'
    elif zeroChoice == 2:
        return 'continue'
    elif zChoice == 3:
        print 'Czy jestes pewien?'
        return 'end'

def zeroChoice():
    zeroCNote = ('1. Wyswietl informacje o programie\n2. '+
    'Wizualizuj depesze\n3. Zamknij program')
    zeroCEAlert = 'Niepoprawnie wprowadzono wybor!'
    zeroChoiceRep = choice(firstNote=zeroCNote, 
                    amountOfSel=3, 
                    errorAlert=zeroCEAlert)
    while zeroChoiceRep[0] != True:
        print zeroChoiceRep[1]
        zeroChoiceRep = choice(firstNote=zeroCNote, 
        amountOfSel=3, errorAlert=zeroCEAlert)
    return zeroChoiceRep[1]

def firstChoice():
    firstCNote = ('1. Wprowadz depesze z pliku\n2. '+
    'Wprowadz depesze z sieci')
    firstCEAlert = 'Niepoprawnie wprowadzono wybor!'
    firstChoiceRep = choice(firstNote=firstCNote, 
                            amountOfSel=2, 
                            errorAlert=firstCEAlert)
    while firstChoiceRep[0] == False:
        print firstChoiceRep[1]
        firstChoiceRep = choice(firstNote=firstCNote, 
                                amountOfSel=2, 
                                errorAlert=firstCEAlert)
    return firstChoiceRep[1]

def getFilePathFromUser():
    try:
        print 'Podaj sciezke do pliku txt, np.: ./dane/plik_z_depeszami.txt '
        filePath = raw_input()
        synop = gS.getSynopFile(path=filePath)
        station = St.Station(synopCode=synop[0], getSynopType='file')
        dateFirst = station.decodeDate()
        wrongDateSum = 0
        for eggs in synop:
            station = St.Station(synopCode=eggs, getSynopType='file')
            date = station.decodeDate()
            if dateFirst == date:
                pass
            else:
                wrongDateSum += 1
        if wrongDateSum > 0:
            print 'Depesze pochodza z roznych okresow, mozliwy bedzie jedynie wydruk pliku Xlsx!'
            rep = synop
            return True,False,rep
        else:
            rep = synop
            return True,True,rep
    except IOError:
        rep = 'Niepoprawnie wprowadzono sciezke do pliku!'
        return False,False,rep
    except IndexError:
        rep = 'Podano pusty plik!'
        return False,False,rep

def firstReactFile():
    rep = getFilePathFromUser()
    while rep[0] != True:
        rep = getFilePathFromUser()
        while rep[1] != True:
            print rep[2]
            rep = getFilePathFromUser()
    return rep[1],rep[2]

def firstReactWeb():
    date = getObservationDateFromUser()
    while date[0] != True:
        print 'Zle wprowadzono date obserwacji'
        date = getObservationDateFromUser()
    try:
        resp = gS.getSynopWeb(startDate=date[1], 
                                endDate=date[1])
        rep = True,resp
    except ur2.URLError:
        print 'Brak polaczenia z internetem!'
        resp = 'Blad sieci'
        rep = False,resp
    return rep

def secondChoice():
    secondCNote = '1. Drukuj plik xlsx\n2. Drukuj wykres wartosci'
    secondCEAlert = 'Niepoprawnie wprowadzono wybor!'
    secondChoiceRep = choice(firstNote=secondCNote, amountOfSel=2, errorAlert=secondCEAlert)
    while secondChoiceRep[0] == False:
        print secondChoiceRep[1]
        secondChoiceRep = choice(firstNote=secondCNote, amountOfSel=2, errorAlert=secondCEAlert)
    return secondChoiceRep[1]

def secondReactXlsx(synop,synopType,fileNameAndPath):
    statList = []
    for eggs in synop:
        station = St.Station(getSynopType=synopType, synopCode=eggs)
        statList.append(station)
    pXR.printXlsx(station=statList, fileName=fileNameAndPath[0], path=fileNameAndPath[1])

def getFileNameFromUser():
    print 'Podaj nazwe pliku wyjsciowego: '
    name = raw_input()
    print 'Podaj sciezke pliku wyjsciowego, np.: ./pliki_wyjsciowe'
    outputPath = raw_input()
    return name,outputPath

def secondAChoice():
    secondACNoteA = '1. Wykres temperatury w stopniach Celsjusza\n2. Wykres temperatury punktu rosy w stopniach Celsjusza'
    secondACNoteB = '\n3. Wykres cisnienia powietrza w hPa na poziomie stacji\n4. Wykres cisnienia powietrza w hPa zrownanego do poziomu morza'
    secondACNote = secondACNoteA+secondACNoteB
    secondACEAlert = 'Niepoprawnie wprowadzono wybor!'
    secondAChoiceRep = choice(firstNote=secondACNote, amountOfSel=4, errorAlert=secondACEAlert)
    while secondAChoiceRep[0] == False:
        print secondAChoiceRep[1]
        secondAChoiceRep = choice(firstNote=secondACNote, amountOfSel=2, errorAlert=secondACEAlert)
    return secondAChoiceRep[1]

def secondAReact():
    obs = secondAChoice()
    if obs == 1:
        return 1,'temp'
    elif obs == 2:
        return 2,'tempPktRos'
    elif obs == 3:
        return 3,'cis'
    elif obs == 4:
        return 4,'cisMor'

def secondReactChart(obsType, synop, synopType, name, path):
    valuesDict = {}
    date = 'YYYYMMDDHHMM'
    for eggs in synop:
        station = St.Station(getSynopType=synopType, synopCode=eggs)
        if obsType[0] == 1:
            valuesDict[station.decodeCityCountry()['miasto']] = station.decodeTemp()
        elif obsType[0] == 2:
            valuesDict[station.decodeCityCountry()['miasto']] = station.decodeDewPointTemp()
        elif obsType[0] == 3:
            valuesDict[station.decodeCityCountry()['miasto']] = station.decodeStationAtmPressure()
        elif obsType[0] == 4:
            valuesDict[station.decodeCityCountry()['miasto']] = station.decodeSeaLvlPressure()
        date = station.decodeDate()
    pC.drawChart(valuesDict=valuesDict, dataType=obsType[1], date=date,fileName=name, outputPath=path)
    return 'Wydrukowano wykres'

def endChoice():
    endCNote = '1. Wroc do poczatku programu\n2. Zamknij program'
    endCEAlert = 'Niepoprawnie wprowadzono wybor!'
    endChoiceRep = choice(firstNote=endCNote, 
                            amountOfSel=2, 
                            errorAlert=endCEAlert)
    while endChoiceRep[0] == False:
        print endChoiceRep[1]
        endChoiceRep = choice(firstNote=endCNote, 
                                amountOfSel=2, 
                                errorAlert=endCEAlert)
    return endChoiceRep[1]

def endChoiceReact():
    eChoice = endChoice()
    if eChoice == 1:
        return 'continue'
    elif eChoice == 2:
        return 'end'

def mainLoop():
    zReact = zeroReact()
    zR = zReact
    if zReact != 'end':
        fC = firstChoice()
        if fC == 1:
            # wprowadzono depesze z pliku
            synop = firstReactFile()
            synopType = 'file'

        elif fC == 2:
            # depesza wprowadzona z sieci
            synop = firstReactWeb()
            while synop[0] != True:
                synop = firstReactWeb()
            synopType = 'web'
        sC = secondChoice()
        if sC == 1:
            # wybrano Xlsx
            cor = False
            while cor != True:
                try:
                    fileNameAndPath = getFileNameFromUser()
                    cor = True
                    secondReactXlsx(synop=synop[1], 
                            synopType=synopType, 
                            fileNameAndPath=fileNameAndPath)
                    print 'Plik znajduje sie w: '+fileNameAndPath[1]
                except IOError:
                    print ('Podany folder nie istnieje!'+
                            ' Wprowadz dane jeszcze raz.')
                    cor = False
        elif sC == 2:
            # wybrano wykres .png
            if synop[0] != True:
                print ('Nie mozna wydrukowac wykresu,' +
                'dane pochodza z roznych okresow!')
            else:
                cor = False
                while cor != True:
                    try:
                        fileNameAndPath = getFileNameFromUser()
                        cor = True
                        sAR = secondAReact()
                        secondReactChart(obsType=sAR, synop=synop[1], 
                                        synopType=synopType, 
                                        name=fileNameAndPath[0], 
                                        path=fileNameAndPath[1])
                    except IOError:
                        cor = False
                        print ('Podany folder nie istnieje,' +
                                ' podaj dane jeszcze raz.')    
        zR = endChoiceReact()
    elif zReact != 'continue':
        zR = endChoiceReact()
    return zR

def main():
    greeting()
    zR = mainLoop()
    while zR != 'end':
        zR = mainLoop()

if __name__=="__main__":
    main()
