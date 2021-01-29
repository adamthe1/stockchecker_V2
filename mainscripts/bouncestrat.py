from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from threading import Thread
import csv
from formain.stochastics import calstochgraph
from formain.ema import calema
from formain.macddone import findmacd, findemaofmacd
from time import time
import pandas as pd
import winsound


def gettickerlist(choice):
    if choice == 0:
        stocklist = []
        targetlist = 'C:\\Users\\adamg\\PycharmProjects\\stocks\\tickerlists\\smp100.csv'
        with open(targetlist, 'r') as stocks:
            stockreader = csv.reader(stocks, delimiter='\n')
            for row in stockreader:
                stocklist.append(row[0])
    elif choice == 1:
        stocklist = []
        targetlist = 'C:\\Users\\adamg\\PycharmProjects\\stocks\\tickerlists\\nasdaq.csv'
        with open(targetlist, 'r') as stocks:
            stockreader = csv.reader(stocks, delimiter='\n')
            for row in stockreader:
                stocklist.append(row[0])
    elif choice == 2:
        stocklist = []
        targetlist = 'C:\\Users\\adamg\\PycharmProjects\\stocks\\tickerlists\\amex.csv'
        with open(targetlist, 'r') as stocks:
            stockreader = csv.reader(stocks, delimiter='\n')
            for row in stockreader:
                stocklist.append(row[0])
    elif choice == 3:
        stocklist = []
        targetlist = 'C:\\Users\\adamg\\PycharmProjects\\stocks\\tickerlists\\nyse.csv'
        with open(targetlist, 'r') as stocks:
            stockreader = csv.reader(stocks, delimiter='\n')
            for row in stockreader:
                stocklist.append(row[0])
    elif choice == 4:
        stocklist = []
        targetlist = 'C:\\Users\\adamg\\PycharmProjects\\stocks\\tickerlists\\stocklist.csv'
        with open(targetlist, 'r') as stocks:
            stockreader = csv.reader(stocks, delimiter='\n')
            for row in stockreader:
                stocklist.append(row[0])
    elif choice == 5:
        stocklist = []
        targetlist = 'C:\\Users\\adamg\\PycharmProjects\\stocks\\tickerlists\\goodvolume.csv'
        with open(targetlist, 'r') as stocks:
            stockreader = csv.reader(stocks, delimiter='\n')
            for row in stockreader:
                stocklist.append(row[0])
    print(stocklist)
    return stocklist


class Data4stocks():
    def __init__(self):
        data1 = None
        data2 = None
        data3 = None
        data4 = None
        data5 = None
        data6 = None
        data7 = None
        data8 = None

data = Data4stocks()  # class to thread 5 stock datas together

emadict = {}


def main():
    firsttime = time()
    marketchoose = 6
    while not 6 > marketchoose > -1:
        marketchoose = int(input('for smp100 press 0 for nasdaq press 1 for amex press 2 for nyse press 3\n '
                                 'for all press 4, for volume over 800000 press 5: '))
    stocklist = gettickerlist(marketchoose)
    # stocklist = ['CMCSA']

    emalist = [18, 50, 100, 200]   # list of all the emas were checking
    global emadict
    """
    
    dictionary of stock names that are viable to the strat by ema
    ex. if AAPL is on a bounce to the 18 today then its added to
    the 18 list
    """
    bounceupstocks = {18: [], 50: [], 100: [], 200: []}
    bouncedownstocks = {18: [], 50: [], 100: [], 200: []}
    impulseupstocks = {'emacutmacd': [], 'emacut': [], 'macdcut': []}
    impulsedownstocks = {'emacutmacd': [], 'emacut': [], 'macdcut': []}
    for spot in range(0, len(stocklist), 8):  # go over all stocks on stocklist
        if spot - 50 > 0:   # shows how close to done
            print(str((spot / len(stocklist)) * 100) + '%', end=', ')
        print(stocklist[spot:spot + 8])
        if len(stocklist) - spot > 8 and len(stocklist) - spot != 0:
            ts = threader(spot, stocklist)  # returns how many threads there are
            for t in range(ts):  # threading so the internet requests go faster
                if len(stocklist) < spot + t:
                    break
                if t == 0:
                    stockdata = data.data1
                elif t == 1:
                    stockdata = data.data2
                elif t == 2:
                    stockdata = data.data3
                elif t == 3:
                    stockdata = data.data4
                elif t == 4:
                    stockdata = data.data5
                elif t == 5:
                    stockdata = data.data6
                elif t == 6:
                    stockdata = data.data7
                elif t == 7:
                    stockdata = data.data8
                if stockdata == 'bad':
                    print('bad')
                    continue
                """
                calculate ema's to check if the stock is on an uptrend or downtrend
                or not at all
                if past 10 days of each is above the bigger one its up
                if below its downtrend else nothing
                """
                try:
                    stockdict = {'open': stockdata[0], 'high': stockdata[1], 'low': stockdata[2], 'close': stockdata[3]}
                    # print(stockdict)
                    p = pd.DataFrame(stockdict)
                    emadict = {6: calema2(6, p), 18: calema2(18, p), 50: calema2(50, p),
                    100: calema2(100, p), 200: calema2(200, p)}
                    # dictionary of ema values

                    up = True  # is uptrend or is downtrend. Is true until proven false
                    down = False  # if is not uptrend it will be true and well check if actually true
                    for i in range(-10, 0):  # check if up is false
                        if not emadict[emalist[0]][i] > emadict[emalist[1]][i] > emadict[emalist[2]][i] > \
                               emadict[emalist[3]][i]:
                            up = False
                            down = True
                            break
                    if down:  # if it might be down check if its not
                        for i in range(-10, 0):  # check if down is false
                            if not emadict[emalist[0]][i] < emadict[emalist[1]][i] < emadict[emalist[2]][i] < \
                                   emadict[emalist[3]][i]:
                                down = False
                                break
                    if up:
                        for emanum in emalist:
                            if meetscriteriaup(stockdata, emanum):
                                bounceupstocks[emanum].append(stockdata[5])
                                print('Long: ', end='')
                                print(bounceupstocks)
                        ispb = isaPBstockup(stockdata)  # check if the stock is an impulse pullback stock
                        if ispb:
                            impulseupstocks[ispb].append(stockdata[5])
                            print('IPup: ', end='')
                            print(impulseupstocks)
                    elif down:
                        for emanum in emalist:
                            if meetscriteriadown(stockdata, emanum):
                                bouncedownstocks[emanum].append(stockdata[5])
                                print('Short: ', end='')
                                print(bouncedownstocks)
                        ispb = isaPBstockdown(stockdata)
                        if ispb:
                            impulsedownstocks[ispb].append(stockdata[5])
                            print('IPdown: ', end='')
                            print(impulsedownstocks)
                except TypeError:
                    continue
                except ZeroDivisionError:
                    continue
                except IndexError:
                    continue
        else:
            for i in range(spot, len(stocklist)):
                stockdata = getdailydata(stocklist[i])
                if stockdata == 'bad':
                    print('bad')
                    continue
                emadict = {18: calema2(18, p), 50: calema2(50, p), 100: calema2(100, p), 200: calema2(200, p)}
                # dictionary of ema values

                up = True  # is uptrend or is downtrend. Is true until proven false
                down = False  # if is not uptrend it will be true and well check if actually true
                for i in range(-10, 0):  # check if up is false
                    if not emadict[emalist[0]][i] < emadict[emalist[1]][i] < emadict[emalist[2]][i] < \
                                emadict[emalist[1]][i]:
                        up = False
                        down = True
                        break
                if down:
                    for i in range(-10, 0):  # check if up is false
                        if not emadict[emalist[0]][i] < emadict[emalist[1]][i] < emadict[emalist[2]][i] < \
                                emadict[emalist[3]][i]:
                               # emadict[emalist[3]][i]:
                            down = False
                            break
                if up:
                    for emanum in emalist:
                        if meetscriteriaup(stockdata, emanum):
                            bounceupstocks[emanum].append(stockdata[5])
                    ispb = isaPBstockup(stockdata)  # check if the stock is an impulse pullback stock
                    if ispb:
                        impulseupstocks[ispb].append(stockdata[5])
                elif down:
                    for emanum in emalist:
                        if meetscriteriadown(stockdata, emanum):
                            bouncedownstocks[emanum].append(stockdata[5])
                    ispb = isaPBstockdown(stockdata)
                    if ispb:
                        impulseupstocks[ispb].append(stockdata[5])
    today = open('C:\\Users\\adamg\\OneDrive\\Documents\\Finance\\today', 'w')

    today.write(f'Long: {bounceupstocks}\n')
    today.write(f'Short: {bouncedownstocks}\n')
    today.write(f'IPup: {impulseupstocks}\n')
    today.write(f'IPdown: {impulsedownstocks}\n')
    print('Long: ', end='')
    print(bounceupstocks)
    print('Short: ', end='')
    print(bouncedownstocks)
    print('IPdown: ', end='')
    print(impulsedownstocks)
    print('IPup: ', end='')
    print(impulseupstocks)
    print(time() - firsttime)
    winsound.Beep(440, 1000)


def meetscriteriaup(stockdata, emanum):
    stockdict = {'open': stockdata[0], 'high': stockdata[1], 'low': stockdata[2], 'close': stockdata[3]}
    macdline, macdsignal = calmacd(stockdict, [50, 100])
    macdgood = False
    if all(a > 0 for a in macdline[-5:]) and all(a > 0 for a in macdsignal[-5:]):
        macdgood = True
    k, d = calstochgraph(stockdata, 5)
    stochgood = False
    if any(i < 30 for i in k[-4:]) and any(i < 38 for i in d[-4:]):
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
    if firstcandle[2] > emadict[emanum][-3]:  # if low of first candle in the pattern is higher than the ema
        if revcandle[2] < emadict[emanum][-2] < revcandle[1]:
            isreverse = True
    elif emadict[emanum][-3] < firstcandle[0] and emadict[emanum][-3] < firstcandle[3]:
        if revcandle[2] < emadict[emanum][-2] < revcandle[1]:
            isreverse = True
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
            if firstcandle[0] > emadict[emanum][-3] > firstcandle[3] and revcandle[0] < emadict[emanum][-2] < revcandle[3]:
                isrev = True
    if not isrev:
        return isrev
    iscfm = False
    if cfmcandle[3] > cfmcandle[0]:
        if cfmcandle[2] > revcandle[2] and cfmcandle[3] > revcandle[1]:
            iscfm = True
    return iscfm


def meetscriteriadown(stockdata, emanum):
    stockdict = {'open': stockdata[0], 'high': stockdata[1], 'low': stockdata[2], 'close': stockdata[3]}
    macdline, macdsignal = calmacd(stockdict, [50, 100])
    macdgood = False
    if all(a < 0 for a in macdline[-5:]) and all(a < 0 for a in macdsignal[-5:]):
        macdgood = True
    k, d = calstochgraph(stockdata, 5)
    stochgood = False
    if any(i > 70 for i in k[-4:]) and any(i > 70 for i in d[-4:]):
        stochgood = True
    isreversal = False  # is the pattern a reversal candle with confirmation
    if isreversaldown(stockdata, emanum) or isttreversaldown(stockdata, emanum):  # first is the 1 or 2 var tt is the t
        isreversal = True  # trade through variation
    if isreversal and macdgood and stochgood:
        return True


def isreversaldown(stockdata, emanum):
    global emadict
    firstcandle = [stockdata[a][-3] for a in range(4)]
    revcandle = [stockdata[a][-2] for a in range(4)]
    cfmcandle = [stockdata[a][-1] for a in range(4)]
    isreverse = False  # is it the start of a reversal pattern without the cfm
    if firstcandle[1] < emadict[emanum][-3]:  # if high of first candle in the pattern is lower than the ema
        if revcandle[1] > emadict[emanum][-2] > revcandle[2]:
            isreverse = True
    elif emadict[emanum][-3] > firstcandle[0] and emadict[emanum][-3] > firstcandle[3]:
        if revcandle[2] < emadict[emanum][-2] < revcandle[1]:
            isreverse = True
    if not isreverse:
        return isreverse
    iscfm = False
    if cfmcandle[3] < cfmcandle[0]:
        if cfmcandle[1] < revcandle[1] and cfmcandle[3] < revcandle[2]:  # if low of cfm is lower than rev and close
            # of cfm is lower than low of rev
            iscfm = True
    return iscfm


def isttreversaldown(stockdata, emanum):
    firstcandle = [stockdata[a][-3] for a in range(4)]
    revcandle = [stockdata[a][-2] for a in range(4)]
    cfmcandle = [stockdata[a][-1] for a in range(4)]
    isrev = False
    if firstcandle[0] < firstcandle[3] and revcandle[0] > revcandle[3]:  # first candle green then revcandle red
        if firstcandle[0] < revcandle[3]:  # open of green lower than close of red
            if firstcandle[0] < emadict[emanum][-3] < firstcandle[3] and revcandle[0] > emadict[emanum][-2] > revcandle[3]:
                isrev = True
    if not isrev:
        return isrev
    iscfm = False
    if cfmcandle[3] < cfmcandle[0]:
        if cfmcandle[1] < revcandle[1] and cfmcandle[3] < revcandle[2]:  # lower high and close lower than low of rev
            iscfm = True
    return iscfm


def isaPBstockup(stockdata):  # did the macd (12, 26, 9) cut up or the 6EMA cut up the 18EMA and has an IP
    global emadict  # get all the emas for the 6 and 18
    stockdict = {'open': stockdata[0], 'high': stockdata[1], 'low': stockdata[2], 'close': stockdata[3]}
    macdline, macdsignal = calmacd(stockdict, [12, 26])
    if emadict[6][-3] < emadict[18][-3] and emadict[6][-2] > emadict[18][-2]:
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
    global emadict  # get the emas for 6 and 18
    stockdict = {'open': stockdata[0], 'high': stockdata[1], 'low': stockdata[2], 'close': stockdata[3]}
    macdline, macdsignal = calmacd(stockdict, [12, 26])
    if emadict[6][-3] > emadict[18][-3] and emadict[6][-2] < emadict[18][-2]:
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


def calmacd(stockdict, nums):
    p = pd.DataFrame(stockdict)
    exp1 = p.close.ewm(span=nums[0], adjust=False).mean()
    exp2 = p.close.ewm(span=nums[1], adjust=False).mean()
    macd = exp1 - exp2
    macdlist = macd.values.tolist()
    exp3 = macd.ewm(span=9, adjust=False).mean()
    signal = exp3.values.tolist()
    return macdlist, signal


def calema2(emanum, pd):
    ema = pd.close.ewm(span=emanum, adjust=False).mean()
    emalist = ema.values.tolist()
    return emalist


def threader(spot, stocklist):
    check = 0
    try:
        t1 = Thread(target=first, args=(stocklist[spot],))
        t2 = Thread(target=second, args=(stocklist[spot + 1],))
        t3 = Thread(target=third, args=(stocklist[spot + 2],))
        t4 = Thread(target=fourth, args=(stocklist[spot + 3],))
        t5 = Thread(target=fifth, args=(stocklist[spot + 4],))
        t6 = Thread(target=sixth, args=(stocklist[spot + 5],))
        t7 = Thread(target=seventh, args=(stocklist[spot + 6],))
        t8 = Thread(target=eight, args=(stocklist[spot + 7],))
        threads = [t1, t2, t3, t4, t5, t6, t7, t8]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print('we out boys')
        exit(-1)
    return len(threads)


def first(stock):
    global data
    data.data1 = getdailydata(stock)


def second(stock):
    global data
    data.data2 = getdailydata(stock)


def third(stock):
    global data
    data.data3 = getdailydata(stock)


def fourth(stock):
    global data
    data.data4 = getdailydata(stock)


def fifth(stock):
    global data
    data.data5 = getdailydata(stock)


def sixth(stock):
    global data
    data.data6 = getdailydata(stock)


def seventh(stock):
    global data
    data.data7 = getdailydata(stock)


def eight(stock):
    global data
    data.data8 = getdailydata(stock)


def getdailydata(name):
    my_share = share.Share(name)
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_MONTH, 50, share.FREQUENCY_TYPE_DAY, 1)
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