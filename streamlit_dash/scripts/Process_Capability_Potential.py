"""
Calculate the Cp & Pp value from a list of values.
input _mylist_ as a standard list of values
ravel is used to ensure 1D array of values

sigma is either the retun value of c_sigma or the p_sigma (mostly the c_sigma)
"""
import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.stats import t

d2 = [0, 1.128, 1.128, 1.693, 2.059, 2.326, 2.534, 2.704, 2.847, 2.970, 3.078, 3.173, 3.258, 3.336, 3.407,
      3.472, 3.532, 3.588, 3.640, 3.689, 3.735, 3.778, 3.819, 3.858, 3.895, 3.931]


def c_sigma(mylist, subgroup=1):  # 1.128 is omdat er geen gemiddelde genomen wordt van samples I-mR graph.
    arr = np.array(mylist).ravel()
    arr = arr[~np.isnan(arr)]
    df = pd.DataFrame({'a': arr})
    df.loc[:, 'shift'] = df[df.columns[0]].shift(1)
    df = df[1:]
    df.loc[:, 'diff'] = abs(df[df.columns[0]] - df[df.columns[1]])
    internal_sigma = df.loc[:, 'diff'].values.mean() / float(d2[subgroup])
    # if internal_sigma == 0:
    #     internal_sigma = 999
    return internal_sigma


def p_sigma(mylist):
    arr = np.array(mylist).ravel()
    arr = arr[~np.isnan(arr)]
    longterm_sigma = arr.std(ddof=1)
    # if longterm_sigma == 0:
    #     longterm_sigma = 999
    return longterm_sigma


def average(mylist):
    arr = np.array(mylist).ravel()
    arr = arr[~np.isnan(arr)]
    return arr.mean()


def processpotential(usl, lsl, sigma):
    potential = abs(float(usl - lsl) / (6*sigma))
    return potential


def processcapability(mylist, usl, lsl, sigma):
    arr = np.array(mylist).ravel()
    arr = arr[~np.isnan(arr)]
    m = np.mean(arr)
    cpu = float(usl - m) / (3*float(sigma))
    cp1 = float(m - lsl) / (3*float(sigma))
    shortterm_processcapability = np.min([cpu, cp1])
    return shortterm_processcapability


def outlier_detect(mylist):
    arr = np.array(mylist).ravel()
    arr = arr[~np.isnan(arr)]
    q1 = np.quantile(arr, 0.25)
    q3 = np.quantile(arr, 0.75)
    whisker = 1.5 * (q3 - q1)
    outlier_down = q1 - whisker
    outlier_up = q3 + whisker
    return outlier_down, outlier_up


def conf_interval(mylist):
    arr = np.array(mylist).ravel()
    arr = arr[~np.isnan(arr)]
    avg = arr.mean()

    # six sigma green belt opleiding
    # std = c_sigma(mylist, subgroup=subgroup)
    # lower = norm.ppf(0.05)
    # upper = norm.ppf(0.95)

    # PID cursus, release 485-524d
    std = arr.std(ddof=1)
    lower = t.ppf(0.025, df=len(arr)-1)
    upper = t.ppf(0.975, df=len(arr)-1)

    lowerbound = avg + lower * (std / (len(arr) ** 0.5))
    upperbound = avg + upper * (std / (len(arr) ** 0.5))

    return avg, lowerbound, upperbound


def test():
    listvar = [23, 19, 17, 18, 24, 26, 21, 14, 18]
    sig_c = c_sigma(listvar)
    sig_p = p_sigma(listvar)
    ucl = 22
    lcl = 15

    print('Cp = %0.2f' % processpotential(ucl, lcl, sig_c))
    print('Cpk  = %0.2f' % processcapability(listvar, ucl, lcl, sig_c))

    print('Pp = %0.2f' % processpotential(ucl, lcl, sig_p))
    print('Ppk  = %0.2f' % processcapability(listvar, ucl, lcl, sig_p))

    out_down, out_up = outlier_detect(listvar)

    print('outlier limit down = %0.2f' % out_down)
    print('outlier limit up = %0.2f' % out_up)

    average, low_bound, up_bound = conf_interval(listvar)

    print('\n99.9CI of the individual measurement of the average %0.2f\n\tlowerbound: %0.2f  \n\tupperbound: %0.2f' %
          (average, low_bound, up_bound))

    average, low_bound, up_bound = conf_interval(listvar)

    print('99.9CI of the average (n=9) measurement of the average %0.2f\n\tlowerbound: %0.2f  \n\tupperbound: %0.2f' %
          (average, low_bound, up_bound))

    print('\nConclusion (six sigma green belt pg.53 part 5: "Beheers" = '
          '\nGemiddelde zal sneller blijk geven van afwijking dan enkele waarden')


if __name__ == '__main__':
    test()

