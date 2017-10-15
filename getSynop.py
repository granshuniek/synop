import urllib
import urllib2

def getSynopWeb(startDate, 
                endDate, 
                country='Pol'):
    ''' Przekazuje liste depesz z sieci OGIMET
        Args:
        startDate=YYYYMMDDHHmm  (mandatory)
        endDate=YYYYMMDDHHmm  (default is current time)
        country=Pol (Polska)
        Format daty:
        YYYY (year, four digits)
        MM (month, two digits)
        DD (day, two digits)
        HH (hour, two digits)
        mm (minute, two digits)'''

    param ={'begin':startDate, 
            'end':endDate, 'state':country, 
            'lang':'eng'}
    url = 'http://www.ogimet.com/cgi-bin/getsynop'
    data = urllib.urlencode(param)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    respRead = response.read()
    resp = respRead.replace('\n', ' ')
    resp = resp.replace(',', ' ')
    synopList = resp.split('=')
    synopNewList = []
    for row in synopList:
        try:
            row = row.split()
            chapterIndex = row.index('333')
            synopNewList.append(row[:chapterIndex])
        except:
            try:
                row = row.split()
                chapterIndex = row.index('555')
                synopNewList.append(row[:chapterIndex])
            except:
                synopNewList.append(row)
    for spam in synopNewList:
        if spam == ' ' or spam == '' or spam == []:
            synopNewList.remove(spam)
    return synopNewList

def getSynopFile(path):
    ''' Przekazuje liste depesz z pliku txt'''
    synopFile = open(path)
    read = synopFile.read()
    read = read.replace('\n', ' ')
    synopList = read.split('=')
    synopFile.close()
    synopNewList = []
    for row in synopList:
        try:
            chapterIndex = row.index('333')
            synopNewList.append(row[:chapterIndex])
        except:
            try:
                chapterIndex = row.index('555')
                synopNewList.append(row[:chapterIndex])
            except:
                synopNewList.append(row)
    for spam in synopNewList:
        if spam == ' ' or spam == '' or spam == []:
            synopNewList.remove(spam)
    return synopNewList
