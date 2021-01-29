import requests
from get_all_tickers import get_tickers as gt
from datetime import datetime
from threading import Thread
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import csv
from time import sleep
from sys import exit

stocklist = []
targetfile = 'C:\\Users\\adamg\\PycharmProjects\\stocks\\tickerlists\\stocklist.csv'
# targetfile = 'smp100.csv'
with open(targetfile, 'r') as stocks:
    stockreader = csv.reader(stocks, delimiter='\n')
    for row in stockreader:
        stocklist.append(row[0])

class data4stocks():
    def __init__(self):
        self.data1 = []
        self.data2 = []
        self.data3 = []
        self.data4 = []
        self.data5 = []
        self.data6 = []

data = data4stocks()
file = open('C:\\Users\\adamg\\PycharmProjects\\stocks\\tickerlists\\goodvolume.csv', 'w')

def main(stocklist):
    try:
        for i in range(0, len(stocklist), 6):
            print(i)
            Thread(target=first, args=(i,)).start()
            Thread(target=second, args=(i+1,)).start()
            Thread(target=third, args=(i+2,)).start()
            Thread(target=fourth, args=(i+3,)).start()
            Thread(target=fifth, args=(i+4,)).start()
            Thread(target=sixth, args=(i+5,)).start()
            sleep(0.15)
    except KeyboardInterrupt:
        print('ok then')
        exit(1)

def first(spot):
    global data
    data.data1 = getdailydata(stocklist[spot])
    if sum(data.data1[6][-15:])/15 > 150000:
        file.write(str(data.data1[5]) + '\n')


def second(spot):
    global data
    data.data2 = getdailydata(stocklist[spot])
    if sum(data.data2[6][-15:])/15 > 150000:
        file.write(str(data.data2[5]) + '\n')

def third(spot):
    global data
    data.data3 = getdailydata(stocklist[spot])
    if sum(data.data3[6][-15:])/15 > 150000:
        file.write(str(data.data3[5]) + '\n')

def fourth(spot):
    global data
    data.data4 = getdailydata(stocklist[spot])
    if sum(data.data4[6][-15:])/15 > 150000:
        file.write(str(data.data4[5]) + '\n')

def fifth(spot):
    global data
    data.data5 = getdailydata(stocklist[spot])
    if sum(data.data5[6][-15:]) / 15 > 150000:
        file.write(str(data.data5[5]) + '\n')

def sixth(spot):
    global data
    data.data6 = getdailydata(stocklist[spot])
    if sum(data.data6[6][-15:]) / 15 > 150000:
        file.write(str(data.data6[5]) + '\n')

def getdailydata(name):
    stockname = name
    my_share = share.Share(stockname)
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_MONTH, 4, share.FREQUENCY_TYPE_DAY, 1)
    except YahooFinanceError as e:
        print(e.message)
        exit(1)
        # print(len(symbol_data['open']))
    return (symbol_data['open'], symbol_data['high'], symbol_data['low'],
           symbol_data['close'], symbol_data['timestamp'], stockname, symbol_data['volume'])




if __name__ == '__main__':
    main(stocklist)