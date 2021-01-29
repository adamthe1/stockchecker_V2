from formain.ema import calema, calsma


# calculate stochastics equation is on the internet
def calstochgraph(data, days):
    smooth = 3
    days = days
    kgraph = []
    for i in range(days, len(data[0])):  # loop over every day so we have value of graph
        c = data[3][i]  # closing price of today
        l14 = min(data[2][i-days+1:i+1])  # lowest price past days
        h14 = max(data[1][i-days+1:i+1])  # highest price past  days
        k = ((c - l14)/(h14 - l14)) * 100
        kgraph.append(k)
    ksmooth = calsma(smooth, kgraph)
    d = calsma(3, ksmooth)
    return ksmooth, d

