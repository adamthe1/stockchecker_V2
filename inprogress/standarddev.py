import numpy as np
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import math
import matplotlib.pyplot as plt

def main():
    data = getdailydata('EXC')
    xpoints = range(len(data[3]))
    ypoints = data[3]
    slope, n, top, bot = regression(xpoints, ypoints)
    print(len(xpoints))
    #  sd = math.sqrt(bot/(len(xpoints)-1))
    sd = calsd(xpoints, ypoints, slope, n)
    plotshow(data)
    x = np.array(range(len(data[0]) + 10))  # show lines on plot
    print(sd, n)
    alpha = 1.5
    yreg = x * slope + n
    ysdup = x * slope + n + (sd * alpha)
    ysddown = x * slope + n - (sd * alpha)
    plt.plot(x, yreg)
    plt.plot(x, ysdup)
    plt.plot(x, ysddown)
    plt.show()

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
    return slope, n, sumtop, sumbot


def calsd(xpoints, ypoints, slope, n):
    sum = 0
    for i in range(len(xpoints)):
        sum += ((ypoints[i] - (slope * xpoints[i] + n)) ** 2)
    sd = math.sqrt(sum / (len(xpoints) - 1))
    return sd


def getdailydata(name):
    stockname = name
    my_share = share.Share(stockname)
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_MONTH, 4, share.FREQUENCY_TYPE_DAY, 1)
    except YahooFinanceError as e:
        print(e.message)
        return 'bad'
    # print(len(symbol_data['open']))
    try:
        if not symbol_data['open']:
            return 'bad'
        return (symbol_data['open'], symbol_data['high'], symbol_data['low'],
                symbol_data['close'], symbol_data['timestamp'], name, symbol_data['volume'])
    except TypeError:
        print(" non subscriptable: " + str(name), end=' ')
        return 'bad'


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

if __name__ == '__main__':
    main()