from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError


def main():
    stockname = str(input('what stock: ').upper())
    print(stockname)
    cfm = -1  # which candle in the graph is the cfm candle
    rev = int(input('which candle is the rev candle (-2, -3, -4): '))
    while True:
        shortorlong = str(input('short or long? (s/l): '))
        if shortorlong == 's':
            break
        if shortorlong == 'l':
            break
    print(shortorlong)
    data = getdailydata(stockname)
    """
    data = list(data)
    for i in [0, 1, 2, 3]:
        data[i] = list(data[i])[:-1]
    """
    amn = 0.03
    if data[3][-1] > 100:
        amn = 0.1
    elif 100 > data[3][-1] > 50:
        amn = 0.05
    elif data[3][-1] < 10:
        amn = 0.01
    while True:
        choice = input('R is from rev or cfm? (r, c): ')
        if choice == 'r':
            break
        if choice == 'c':
            break
    if shortorlong == 'l':
        if choice == 'r':
            r = (data[1][cfm] + amn) - (data[2][rev] - amn)
        if choice == 'c':
            r = (data[1][cfm] + amn) - (data[2][cfm] - amn)
    elif shortorlong == 's':
        if choice == 'r':
            r = (data[1][rev] + amn) - (data[2][cfm] - amn)
        if choice == 'c':
            r = (data[1][cfm] + amn) - (data[2][cfm] - amn)
    else:
        r = 'error'
    print('R =' + str(r))
    print('ATR: ' + str(getATRavg(data)))

    risk = float(input('risk per trade: ')) / 100
    capital = float(input('capital: '))
    numofshares = (risk * capital) / r
    print('num of shares: ' + str(numofshares))
    print('amount in $: ' + str(numofshares * (data[3][-1] + amn)), end='\n\n')
    print('rounded: ' + str(round(numofshares)))
    print('amount in $ rounded: ' + str(round(numofshares) * (data[3][-1] + amn)))
    newrisk = ((round(numofshares) * r) / capital) * 100
    print('newrisk per trade: ' + str(newrisk), end='\n\n')

    rmultiple = 2.5
    if shortorlong == 'l':
        print('entry: ' + str(data[1][-1] + amn))
        print('stoploss(rev): ' + str(data[2][rev] - amn) + ', or stoploss(cfm): ' + str(data[2][cfm] - amn))
        print('takeprofit: ' + str(data[1][cfm] + r * rmultiple))
    elif shortorlong == 's':
        print('entry: ' + str(data[2][-1] - amn))
        print('stoploss(rev): ' + str(data[1][rev] + amn) + ', or stoploss(cfm): ' + str(data[1][cfm] + amn))
        print('takeprofit: ' + str(data[2][cfm] - r * rmultiple))


def getATRavg(data):
    opens, high, low, close = data[0:4]
    trlist = []
    for spot in range(len(high)):
        tr = max(high[spot] - low[spot], abs(high[spot] - close[spot - 1]), abs(low[spot] - close[spot - 1]))
        trlist.append(tr)

    # calculate atr they should all be same len
    atrlist = atr(trlist)
    l = 60
    return sum(atrlist[-l:]) / l


def atr(list):
    period = 14
    atrlist = []
    didfirst = False
    for spot, item in enumerate(list):
        if spot < period:
            continue
        if not didfirst:
            atr = (list[spot - 1] * (period - 1) + item) / period
            atrlist.append(atr)
            didfirst = True
        else:
            atr = (atrlist[-1] * (period - 1) + item) / period
            atrlist.append(atr)
    # print(atrlist)
    return atrlist


def getdailydata(name):
    my_share = share.Share(name)
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_MONTH, 1, share.FREQUENCY_TYPE_DAY, 1)
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
