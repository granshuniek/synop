from PIL import Image, ImageDraw, ImageFont

def createImage(high, width):
    im = Image.new('RGB', (width,high), 'white')
    return im

def saveImage(fileNameOutputPath,im):
    im.save(fileNameOutputPath)
    im.close()

def observationType(dataType):
    if dataType == 'temp':
        return 'Temperatura w stopniach Celsjusza'
    elif dataType == 'tempPktRos':
        return 'Temperatura punktu rosy w stopniach Celsjusza'
    elif dataType == 'cis':
        return 'Cisnienie na poziomie stacji synoptycznej'
    elif dataType == 'cisMor':
        return 'Cisnienie zrownane do poziomu morza'
        
def countChartVariables(maxV, minV, lCol):
    if maxV < 0:
        wCol = -1*(0.2*minV)
        iMU = -1*(0.2*minV)
        hWU = iMU
        wB = -1*(0.3*minV)
        wW = -1*((wB*(lCol+1)) + (lCol*wCol))
        marginOut = -1*(0.2*minV)
        if minV < 0:
            hWL = iMU+(-1*minV)
        else:
            hWL = iMU
        hImage = int((2*marginOut)+hWU+hWL)
        wImage = -1*(int((2*marginOut)+wW))
        fntSize = -1*(int(minV*0.05))
        return hWU,wB,wW,marginOut,hImage,wImage,hWL,iMU,wCol,fntSize
    else:
        wCol = 0.2*maxV
        iMU = 0.2*maxV
        hWU = iMU+maxV
        wB = 0.3*maxV
        wW = (wB*(lCol+1)) + (lCol*wCol)
        marginOut = 0.2*maxV
        if minV < 0:
            hWL = iMU+(-1*minV)
        else:
            hWL = iMU
        hImage = int((2*marginOut)+hWU+hWL)
        wImage = int((2*marginOut)+wW)
        fntSize = int(maxV*0.05)
        return hWU,wB,wW,marginOut,hImage,wImage,hWL,iMU,wCol,fntSize

def drawChart(valuesDict, dataType, 
                date, fileName, 
                outputPath='./pliki_wyjsciowe'):
    valuesList = []
    noDataList = []
    for key in valuesDict:
        if dataType == 'temp' or dataType == 'tempPktRos':
            try:
                valuesList.append(float(valuesDict[key])*100)
            except ValueError:
                #gdy brak obserwacji
                noDataList.append(key)
        elif dataType == 'cis' or dataType == 'cisMor':
            try:
                valuesList.append(float(valuesDict[key]))
            except ValueError:
                #gdy brak obserwacji
                noDataList.append(key)

    fileNameOutputPath = outputPath + '/' + fileName + '.png'

    maxV = max(valuesList)
    minV = min(valuesList)
    lCol = len(valuesList)

    wVariables = countChartVariables(maxV, 
                    minV, lCol)
    hWU = wVariables[0]
    wB = wVariables[1]
    wW = wVariables[2]
    marginOut = wVariables[3]
    hImage = wVariables[4]
    wImage = wVariables[5]
    hWL = wVariables[6]
    iMU = wVariables[7]
    wCol = wVariables[8]
    fntSize = wVariables[9]

    im = createImage(hImage, wImage)
    draw = ImageDraw.Draw(im)

    startXzero = marginOut
    startYzero = marginOut+hWU

    step = wB+wCol

    fnt = ImageFont.truetype('./fonts/raleway.ttf', 
                                size=fntSize)

    # parametry dla osi wykresu
    # os pionowa Y
    startYFenceX = marginOut
    startYFenceY = marginOut+(0.5*iMU)
    endYFenceX = marginOut
    endYFenceY = startYzero+hWL
    # os pozioma X
    startXFenceX = marginOut
    startXFenceY = startYzero
    endXFenceX = marginOut+wW
    if maxV < 0:
        endXFenceX = marginOut+(-1*wW)
    endXFenceY = startYzero

    # notatka o typie obserwcji i datcie jej wykonania
    adnotation = observationType(dataType)+'  '+date

    # czesc rysujaca
    print 'Drukuje wykres, prosze poczekac chwile.'
    for key in valuesDict:
        if dataType == 'temp' or dataType == 'tempPktRos':
            try:
                value = (-1*float
                (valuesDict[key]))*100
                draw.rectangle([(startXzero+wB,
                                startYzero+value), 
                                (startXzero+wB+wCol, 
                                startYzero)], outline=1, fill='red')
                draw.text(xy=(startXzero+wB, 
                              startYzero-hWU), 
                              text=str(valuesDict[key]), 
                              fill='black', font=fnt)
                draw.text(xy=(startXzero+wB, 
                              startYzero+(0.3*marginOut)+hWL), 
                              text=key,
                              fill='black', font=fnt)
                startXzero += step
            except ValueError:
                # brak obserwacji
                print 'Brak obserwacji dla stacji: ' + key
        else:
            try:
                value = (-1*float(valuesDict[key]))
                draw.rectangle([(startXzero+wB,startYzero+value), 
                                (startXzero+wB+wCol, 
                                 startYzero)], outline=1, 
                                 fill='green')
                draw.text(xy=(startXzero+wB, 
                                startYzero-hWU), 
                                text=str(valuesDict[key]), 
                                fill='black', font=fnt)
                draw.text(xy=(startXzero+wB, 
                                startYzero+
                                (0.3*marginOut)+hWL), 
                                text=key, fill='black', 
                                font=fnt)
                startXzero += step
            except ValueError:
                #gdy brak obserwacji
                if valuesDict[key] == 'Zabronione':
                    print ('Stacja '+key+
                    ' nie moze podac cisnienia' + 
                    ' zrownanego do poziomu morza.')
                else:
                    print 'Brak obserwacji dla stacji: ' + key
    startXzero = marginOut
    draw.text(xy=(0.2*startXzero, 0.2*startXzero), 
                text=adnotation, fill='black', font=fnt)
    draw.line([(startYFenceX, startYFenceY), 
                (endYFenceX, endYFenceY)], fill='black', width=4)
    draw.line([(startXFenceX, startXFenceY), 
                (endXFenceX, endXFenceY)], fill='black', width=4)

    saveImage(fileNameOutputPath=fileNameOutputPath, im=im)
    print 'Wykres znajduje sie w '+fileNameOutputPath
