# import Station as sU
# import printXlsxReport as dV
# import getSynop as gS
#
#
# statList = []
# synopList = gS.getSynopFile('dane/synop_test2.txt')
# # for spam in synopList:
# #     if spam == ' ' or spam == '':
# #         synopList.remove(spam)
# for spam in synopList:
#     stacja = sU.Station(getSynopType='file', synopCode=spam)
#     statList.append(stacja)
# dV.printXlsx(station=statList, fileName='testV2')
#
#
#
#
#

# stacja = gS.getSynopWeb(dataRozp='201605210000', dataZakon='201605220001')
# stacjaObiekt = sU.Stacja(depesza=stacja[0], getSynopType='web')
# statList =[]
# for spam in stacja:
#     stacja = sU.Stacja(depesza=spam, getSynopType='web')
#     statList.append(stacja)
#
#
#
# dV.drukujXlsx(stacja=statList, nazwa='web_sec_test.xslx')
import urrlib, urrlib2

param ={'begin':startDate, 'end':endDate, 'state':country, 'lang':'eng'}
url = 'http://www.ogimet.com/cgi-bin/getsynop'
data = urllib.urlencode(param)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
respRead = response.read()
