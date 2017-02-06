import numpy as np

def otsu_threshold(values, bins):
    hist = np.histogram(values, bins)
    hist_values = hist[0]
    hist_bins = hist[1]
    threshold = 0
    sumB = 0
    wB, wF = 0, 0
    maximum = 0
    total = len(values)
    sum_all = 0
    for t in range(len(hist_values)):
        sum_all += t*hist_values[t]
    for t in range(len(hist_values)):
        wB += hist_values[t]
        if wB == 0:
            continue
        wF = total - wB
        if wF == 0:
            break
        sumB += t * hist_values[t]
        meanB = sumB/wB
        meanF = (sum_all - sumB)/wF
        var = wB*wF*(meanB - meanF)**2
        if var>=maximum:
            threshold = t
            maximum = var

    return (hist_bins[threshold] + hist_bins[min(threshold+1, len(hist_bins))])/2