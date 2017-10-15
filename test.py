# import printChart as pC
# import stacjaUniversal as sU
# import getSynop as gS
#
# listaStacji = []
# slownikDoWizualizacji = {}
# sprawdzarkaPowtorek = []
#
# depesza = gS.getSynopWeb(startDate='201605101000', endDate='201605101000')
#
# date = '201608190000'
# for spam in depesza:
#     station = sU.Station(getSynopType='web', synopCode=spam)
#     slownikDoWizualizacji[station.decodeCityCountry()['miasto']] = station.decodeTemp()
#     date = station.decodeDate()
#
# pC.drawChart(valuesDict=slownikDoWizualizacji, dataType='temp', date=date, fileName='angWykr.png')
'''
def getFilePathFromUser():
    try:
        print 'Podaj sciezke do pliku txt, np.: dane/plik_z_depeszami.txt '
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
            elif:
                wrongDateSum += 1
        if wrongDateSum > 0:
            rep = 'Depesze pochodza z roznych okresow'
            return False,rep
        else:
            rep = synop
            return True,rep
    except IOError:
        rep = 'Brak sciezki'
        print 'Niepoprawnie wprowadzono sciezke do pliku!'
        return False,rep


def checkFileSynopDate(synopFromFile):
    synop = synopFromFile
    station = St.Station(synopCode=synop[0], getSynopType='file')
    date = str(station.decodeDate())
    errorSum = 0
    for eggs in synop:
        station = St.Station(synopCode=eggs, getSynopType='file')
        if date != str(station.decodeDate()):
            print date
            errorSum += 1
    if errorSum == 0:
        return True
    else:
        print 'Depesze pochodza z roznych okresow czasu!'
        return Fals




if choiceCzwarty[1] == 1:
    for spam in depesza:
        station = sU.Stacja(getSynopType='web', depesza=spam)
        slownikDoWizualizacji[station.dekodujMiastoPanstwo()['miasto']] = station.dekodujTemp()
        date = station.dekodujDate()
    pC.rysujWykr(valuesDict=slownikDoWizualizacji, dataType='temp', date=date, nazwa=nazwa)
if choiceCzwarty[1] == 2:
    for spam in depesza:
        station = sU.Stacja(getSynopType='web', depesza=spam)
        slownikDoWizualizacji[station.dekodujMiastoPanstwo()['miasto']] = station.dekodujTempPktRos()
        date = station.dekodujDate()
    pC.rysujWykr(valuesDict=slownikDoWizualizacji, dataType='tempPktRos', date=date, nazwa=nazwa)
if choiceCzwarty[1] == 3:
    for spam in depesza:
        station = sU.Stacja(getSynopType='web', depesza=spam)
        slownikDoWizualizacji[station.dekodujMiastoPanstwo()['miasto']] = station.dekodujCisnienieNaPoziomieStacji()
        date = station.dekodujDate()
    pC.rysujWykr(valuesDict=slownikDoWizualizacji, dataType='cis', date=date, nazwa=nazwa)
if choiceCzwarty[1] == 4:
    for spam in depesza:
        station = sU.Stacja(getSynopType='web', depesza=spam)
        slownikDoWizualizacji[station.dekodujMiastoPanstwo()['miasto']] = station.dekodujCisNaPozMorza
        date = station.dekodujDate()
    pC.rysujWykr(valuesDict=slownikDoWizualizacji, dataType='cisMor', date=date, nazwa=nazwa)





'''
import getSynop as gS
print gS.getSynopWeb(startDate='2016', endDate='201208221700')[0]
