def calema(emadays, values):  # emadays= how many days to check values = close values of stock or numbers check ema of
    sma = calsma(emadays, values)
    closepoints = values
    ema = []
    smoothing = 2
    for points in range(emadays, len(closepoints)):
        if not ema:
            ematoday = (closepoints[points] * (smoothing/(1 + emadays))) + sma[points - emadays] * (1 - (smoothing/(1 + emadays)))
            ema.append(ematoday)
        else:
            ematoday = (closepoints[points] * (smoothing/(1 + emadays))) + \
                       ema[points - emadays - 1] * (1 - (smoothing/(1 + emadays)))
            ema.append(ematoday)
    return ema


def calsma(smadays, values):  # smadays= how many days to check values = close values of stock or numbers check sma of
    closepoints = values
    sma = []
    for days in range(smadays, len(closepoints)):
        sumsma = 0
        amount = 0
        for i in range(days - smadays + 1, days + 1):
            sumsma += float(closepoints[i])
            amount += 1
        sma.append(sumsma/amount)
    return sma