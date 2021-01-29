import matplotlib.pyplot as plt
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import numpy as np
from formain.eater import eater
from formain.findhammers import ishammer
from formain.macddone import findmacd, findemaofmacd
from mainscripts.trendline import getgoodeqs
from datetime import datetime
import csv


class stock:
    def __init__(self, stockdata):
        self.stockdata = stockdata

        # get all data needed from stockdata
        self.openpoints = stockdata[0]
        self.highpoints = stockdata[1]
        self.lowpoints = stockdata[2]
        self.closepoints = stockdata[3]
        self.volume = stockdata[6]

        self.checkdays = 5
        self.gethammerlist()
        self.geteaterlist()

        self.goodeqs = getgoodeqs(stockdata)  # find the eqs that are trendline and parallel
        self.topeqs = list(self.goodeqs[0])  # split them into top and bot
        self.boteqs = list(self.goodeqs[1])
        # print(self.topeqs[0].nums)

        self.macd = findmacd(stockdata)  # get macd
        self.emamacd = findemaofmacd(self.macd, 9)
        for i in range(len(self.macd) - len(self.emamacd)):  # fix length macd
            self.macd.pop(0)

    def gethammerlist(self):
        self.hammerlist = []
        for i in range(self.checkdays, 0, -1):
            spotdata = [self.openpoints[-i], self.highpoints[-i], self.lowpoints[-i], self.closepoints[-i]]
            self.hammerlist.append(ishammer(spotdata))

    def geteaterlist(self):
        x = - self.checkdays - 1
        checklist = [self.openpoints[x:], self.highpoints[x:], self.lowpoints[x:],
                     self.closepoints[x:]]  # the first one isnt checked but is needed
        self.eaterlist = eater(checklist)
        self.eaterlist.pop(0)  # because first one wasnt even checked so we need only past checkdays days


"""
class Line
num is the value of the res or sup line, points is the three extremums that compose it
maxpoints is the list of maxpoints values in the graph.
a function will find all extra extremums close to it.

receives (value, 3 spot of points in the extremum list that compose it,
          string of 'r' or 's' that means resistance or support, 
          all max or min values, all max or min points) 
"""


class Line:
    def __init__(self, num, points, ressup, extvalues, extspots):
        self.value = num
        self.expoints = points  # extremum points
        self.ressup = ressup
        self.extvalues = extvalues  # their value in the graph
        self.extspots = extspots  # their spot in the graph
        self.extraex = []  # gets all extra extremum points close to line (their spot in the extremum lists)
        self.extrapoints()  # function to find extra extremums (list)

    @property
    def num(self):
        return len(self.extraex) + 3

    def extrapoints(self):
        if self.expoints[2] + 1 == len(self.extvalues):
            return False
        for i in range(self.expoints[2] + 1, len(self.extvalues)):
            if abs(self.value - self.extvalues[i]) < self.value * 0.02:
                self.extraex.append(i)


# listofstocks = []
stocklist = []
# targetlist = 'stocklist.csv'
targetlist = 'smp100.csv'

with open(targetlist, 'r') as stocks:
    stockreader = csv.reader(stocks, delimiter='\n')
    for row in stockreader:
        stocklist.append(row[0])


def main():
    listofstocks = []
    data = getdailydata('CVS')
    highpoints = data[1]
    lowpoints = data[2]
    maxima = findmax(highpoints)
    minima = findmin(lowpoints)
    maxhighpoints = []
    minlowpoints = []
    for point in maxima:  # add value of maximum point
        maxhighpoints.append(highpoints[point])
    # for point in minima:  # add value of minimum point
    #    minlowpoints.append(lowpoints[point])
    print(maxhighpoints)
    lines = resistance(data, maxhighpoints)
    if not lines:
        print('no resistance')
        exit(1)
    plotshow(data)
    print(lines)
    num = 5
    yvalues = [lines[num][0], lines[num][0]]
    xvalues = [maxima[lines[num][1][0]] - 5, maxima[lines[num][1][2]] + 5]
    plt.plot(xvalues, yvalues, linewidth=2, color='black')
    plt.show()


def resistance(data, maxpoints):
    lines = []
    for i in range(len(maxpoints) - 2):  # go over all maxpoint values except last 2 cause its a triple loop
        for j in range(i + 1, i + 4):
            for t in range(j + 1, j + 4):
                if t > len(maxpoints) - 1:
                    break
                value1, value2, value3 = maxpoints[i], maxpoints[j], maxpoints[t]
                avg = (value1 + value2 + value3) / 3
                if abs(value1 - avg) < value1 * 0.015 and abs(value2 - avg) < value2 * 0.015 \
                        and abs(value3 - avg) < value3 * 0.02:
                    line = Line(avg, [i, j, t])
                    lines.append()
            if j == len(maxpoints) - 1:
                break
    return lines


extfac = 4


def findmax(points):
    maximums = []
    for i in range(len(points) - extfac):
        if i < extfac - 1:
            continue
        checker = []
        for j in range(-1 * extfac, extfac + 1):
            checker.append(points[i + j])
        if checker.index(max(checker)) == extfac:
            maximums.append(i)
    return maximums


def findmin(points):
    minimums = []
    for i in range(len(points) - extfac):
        if i < extfac - 1:
            continue
        checker = []
        for j in range(-extfac, extfac + 1):
            checker.append(points[i + j])
        if checker.index(min(checker)) == extfac:
            minimums.append(i)


def regression(listpointsx, listpointsy):
    meanx = np.mean(listpointsx)
    meany = np.mean(listpointsy)
    sumtop = 0
    sumbot = 0
    for i in range(len(listpointsx)):
        sumtop += (listpointsx[i] - meanx) * (listpointsy[i] - meany)
        sumbot += (listpointsx[i] - meanx) ** 2
    slope = sumtop / sumbot
    n = meany - meanx * slope
    return slope, n


def plotshow(them):  # show graph of stock in candles them is data
    for spot in range(len(them[0])):
        firstpointx = spot
        secondpointx = spot
        firstpointy = them[1][spot]
        secondpointy = them[2][spot]
        yvalues = [firstpointy, secondpointy]
        xvalues = [firstpointx, secondpointx]
        plt.plot(xvalues, yvalues, linewidth=1, color='black')
        firstpointy = them[0][spot]
        secondpointy = them[3][spot]
        yvalues = [firstpointy, secondpointy]
        volumevalue = them[4][spot]
        if firstpointy < 10:
            amount = 1
        elif firstpointy < 100:
            amount = 10
        else:
            amount = 100
        while int(volumevalue / amount) > 0:
            volumevalue = volumevalue / 10
        yvolumevalues = (0, volumevalue)
        if firstpointy > secondpointy:
            plt.plot(xvalues, yvalues, linewidth=5, color='red')
            plt.plot(xvalues, yvolumevalues, linewidth=3, color='red')
        else:
            plt.plot(xvalues, yvalues, linewidth=5, color='green')
            plt.plot(xvalues, yvolumevalues, linewidth=3, color='green')
        firstpointy = them[2][spot]
        secondpointy = them[3][spot]
        yvalues = [firstpointy, secondpointy]
        plt.plot(xvalues, yvalues, linewidth=1, color='black')


def getdailydata(name):
    my_share = share.Share(name)
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_MONTH, 6, share.FREQUENCY_TYPE_DAY, 1)
    except YahooFinanceError as e:
        print(e.message)
        return 'bad'
    # print(len(symbol_data['open']))
    return (symbol_data['open'], symbol_data['high'], symbol_data['low'],
            symbol_data['close'], symbol_data['timestamp'], name, symbol_data['volume'])


def getfourhourdata(name):
    my_share = share.Share(name)
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY, 30, share.FREQUENCY_TYPE_MINUTE, 60)
    except YahooFinanceError as e:
        print(e.message)
        return 'bad'
    goodhoursspot = []
    for i in range(len(symbol_data['timestamp'])):
        strdata = str(datetime.fromtimestamp(symbol_data['timestamp'][i] / 1000))
        checker = strdata[14]
        if checker == '3':
            goodhoursspot.append(i)
    # print(goodhoursspot)
    # print(symbol_data['open'][5])
    goodopenprices = []
    goodhighprices = []
    goodlowprices = []
    goodcloseprices = []
    goodhours = []
    goodvolumes = []
    keep = 0
    for i in goodhoursspot:
        if keep == 7:
            keep = 0
        if keep == 0 or keep == 4:
            if keep == 0:
                high = max(symbol_data['high'][i:i + 4])
                low = min(symbol_data['low'][i:i + 4])
            if keep == 4:
                high = max(symbol_data['high'][i:i + 3])
                low = min(symbol_data['low'][i:i + 3])
            # print(str(datetime.fromtimestamp(symbol_data['timestamp'][i] / 1000)))
            goodopenprices.append(symbol_data['open'][i])
            goodhighprices.append(high)
            goodlowprices.append(low)
            goodcloseprices.append(symbol_data['close'][i])
            goodhours.append(symbol_data['timestamp'][i])
            goodvolumes.append(symbol_data['volume'][i])
        keep += 1
    # print(goodopenprices, goodhighprices, goodlowprices, goodcloseprices)
    return goodopenprices, goodhighprices, goodlowprices, goodcloseprices, goodhours, name, goodvolumes


if __name__ == '__main__':
    main()
