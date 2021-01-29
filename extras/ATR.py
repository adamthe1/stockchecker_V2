from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError


def main():
    data = getdailydata(input('Stock name Pls: ').upper())
    opens, high, low, close = data[0:4]
    trlist = []
    for spot in range(len(high)):
        tr = max(high[spot] - low[spot], abs(high[spot] - close[spot - 1]), abs(low[spot] - close[spot - 1]))
        trlist.append(tr)

    # calculate atr they should all be same len
    atrlist = atr(trlist)
    l = 60
    print(sum(atrlist[-l:])/l)


def atr(list):
    period = 14
    atrlist = []
    didfirst = False
    for spot, item in enumerate(list):
        if spot < period:
            continue
        if not didfirst:
            atr = (list[spot - 1] * (period - 1) + item)/period
            atrlist.append(atr)
            didfirst = True
        else:
            atr = (atrlist[-1] * (period - 1) + item)/period
            atrlist.append(atr)
    # print(atrlist)
    return atrlist


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


if __name__ == '__main__':
    main()