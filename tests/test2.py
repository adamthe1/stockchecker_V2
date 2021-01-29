from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import pprint
import csv
from time import time
from formain.stochastics import calstochgraph
from formain.ema import calema
from formain.macddone import findmacd, findemaofmacd
from mainscripts.trendline import showcandles
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


stocklist = []
targetlist = 'C:\\Users\\adamg\\PycharmProjects\\stocks\\tickerlists\\smp100.csv'
with open(targetlist, 'r') as stocks:
    stockreader = csv.reader(stocks, delimiter='\n')
    for row in stockreader:
        stocklist.append(row[0])


emadict = {}
ema50test = []

def main():
    global emadict, ema50test, ema6testPB, ema18testPB
    stockdata = getdailydata('SWM')
    print(stockdata[2])
    them = list(stockdata[0:4])
    them.append(stockdata[6])
    emadict = {6: calema(6, stockdata[3]), 18: calema(18, stockdata[3]), 50: calema(50, stockdata[3]), 100: calema(100, stockdata[3]),
               200: calema(200, stockdata[3])}  # dictionary of ema values
    ilist = []
    PBlist = []
    for i in range(105, len(stockdata[0])):
        ema6testPB = emadict[6][:i - 6]
        ema18testPB = emadict[18][:i - 18]
        ema50test = emadict[50][:i - 50]
        thedata = [stockdata[0][:i], stockdata[1][:i], stockdata[2][:i], stockdata[3][:i]]
        # print(len(stockdata[0][:i]))
        # if meetscriteriaup(thedata, 18):
         #   ilist.append(i - 1)
        if isaPBstockdown(thedata):
            PBlist.append(i - 1)
    showcandles(them)
    ema50test = emadict[50]
    ema6testPB = emadict[6]
    ema18testPB = emadict[18]
    ilistvals = []
    PBlistvals = []
    #  print(ilist)
    #  print(stockdata[4][ilist[0]]) # for a in ilist)
    """
    for i in ilist:
        ilistvals.append(stockdata[3][i] + 10)
    plt.plot(range(50, 50 + len(ema50test)), ema50test)
    plt.scatter(ilist, ilistvals, color='red')
    """
    print(PBlist)
    for i in PBlist:
        timestamp = stockdata[4][i] / 1000
        dt_object = datetime.fromtimestamp(timestamp)
        print(dt_object)
    plt.show()


def meetscriteriaup(stockdata, emanum):
    stockdict = {'open': stockdata[0], 'high': stockdata[1], 'low': stockdata[2], 'close': stockdata[3]}
    macdline, macdsignal = calmacd(stockdict, [50, 100])
    macdgood = False
    if all(a > 0 for a in macdline[-5:]) and all(a > 0 for a in macdsignal[-5:]):
        macdgood = True
    k, d = calstochgraph(stockdata, 5)
    stochgood = False
    if any(i < 30 for i in k[-4:]) and any(i < 30 for i in d[-4:]):
        stochgood = True
    isreversal = False  # is the pattern a reversal candle with confirmation
    if isreversalup(stockdata, emanum) or isttreversalup(stockdata, emanum):  # first is the 1 or 2 var tt is the t
        isreversal = True                                                     # trade through variation
    if isreversal and macdgood and stochgood:
        return True


def isreversalup(stockdata, emanum):
    global emadict
    firstcandle = [stockdata[a][-3] for a in range(4)]
    revcandle = [stockdata[a][-2] for a in range(4)]
    cfmcandle = [stockdata[a][-1] for a in range(4)]
    isreverse = False  # is it the start of a reversal pattern without the cfm
    if firstcandle[2] > ema50test[-3]:  # if low of first candle in the pattern is higher than the ema
        if firstcandle[1] > revcandle[0] and firstcandle[1] > revcandle[3]:  # if high first candle is higher than
            # body of rev
            if revcandle[2] < ema50test[-2] < revcandle[1]:
                isreverse = True
                # print('first is true: ')
    elif ema50test[-3] < firstcandle[0] and ema50test[-3] < firstcandle[3]:
        if firstcandle[1] > revcandle[0] and firstcandle[1] > revcandle[3]:
            if revcandle[2] < ema50test[-2] < revcandle[1]:
                isreverse = True
                # print('second is true')
    if not isreverse:
        return isreverse
    iscfm = False
    if cfmcandle[3] > cfmcandle[0]:
        if cfmcandle[2] > revcandle[2] and cfmcandle[3] > revcandle[1]:
            iscfm = True
    return iscfm


def isttreversalup(stockdata, emanum):
    firstcandle = [stockdata[a][-3] for a in range(4)]
    revcandle = [stockdata[a][-2] for a in range(4)]
    cfmcandle = [stockdata[a][-1] for a in range(4)]
    isrev = False
    if firstcandle[0] > firstcandle[3] and revcandle[0] < revcandle[3]:  #first candle red then revcandle green
        if firstcandle[0] > revcandle[3]:  # open of red higher than close of green
            if firstcandle[0] > ema50test[-3] > firstcandle[3] and revcandle[0] < ema50test[-2] < revcandle[3]:
                isrev = True
    if not isrev:
        return isrev
    iscfm = False
    if cfmcandle[3] > cfmcandle[0]:
        if cfmcandle[2] > revcandle[2] and cfmcandle[3] > revcandle[1]:
            iscfm = True
    return iscfm


def isaPBstockup(stockdata):  # did the macd (12, 26, 9) cut up or the 6EMA cut up the 18EMA and has an IP
    global emadict,  ema6testPB, ema18testPB  # get all the emas for the 6 and 18
    stockdict = {'open': stockdata[0], 'high': stockdata[1], 'low': stockdata[2], 'close': stockdata[3]}
    macdline, macdsignal = calmacd(stockdict, [12, 26])
    if ema6testPB[-3] < ema18testPB[-3] and ema6testPB[-2] > ema18testPB[-2]:
        if isPBup(stockdata):
            if macdline[-1] > macdsignal[-1]:
                return 'emacutmacd'
            else:
                return 'emacut'
    if macdline[-3] < macdsignal[-3] and macdline[-2] > macdsignal[-2]:
        if isPBup(stockdata):
            return 'macdcut'
    return False


def isPBup(stockdata):  # check is there a pullback in the stock or at least an inside candle
    if stockdata[1][-3] < stockdata[1][-2] > stockdata[1][-1]:
        return True
    return False


def isaPBstockdown(stockdata):  # is an IP stock for short
    global emadict,  ema6testPB, ema18testPB  # get all the emas for the 6 and 18
    stockdict = {'open': stockdata[0], 'high': stockdata[1], 'low': stockdata[2], 'close': stockdata[3]}
    macdline, macdsignal = calmacd(stockdict, [12, 26])
    if ema6testPB[-3] > ema18testPB[-3] and ema6testPB[-2] < ema18testPB[-2]:
        if isPBdown(stockdata):
            if macdline[-1] < macdsignal[-1]:
                return 'emacutmacd'
            else:
                return 'emacut'
    if macdline[-3] > macdsignal[-3] and macdline[-2] < macdsignal[-2]:
        if isPBdown(stockdata):
            return 'macdcut'
    return False


def isPBdown(stockdata):
    if stockdata[2][-3] > stockdata[2][-2] < stockdata[2][-1]:
        return True
    return False


def calema2(emadays, p):  # emadays= how many days to check values = close values of stock or numbers check ema of
    ema = p.close.ewm(span=emadays, adjust=False).mean()
    emalist = ema.values.tolist()
    return emalist


def calmacd(stockdict, nums):
    p = pd.DataFrame(stockdict)
    exp1 = p.close.ewm(span=nums[0], adjust=False).mean()
    exp2 = p.close.ewm(span=nums[1], adjust=False).mean()
    macd = exp1 - exp2
    macdlist = macd.values.tolist()
    exp3 = macd.ewm(span=9, adjust=False).mean()
    signal = exp3.values.tolist()
    return macdlist, signal


def getdailydata(name):
    my_share = share.Share(name)
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_MONTH, 80, share.FREQUENCY_TYPE_DAY, 1)
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

if __name__ == "__main__":
    main()
