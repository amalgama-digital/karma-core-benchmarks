__author__ = 'denn'

from KarmaApi import curve_regression

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
import np
import json

import getopt, sys

my_dpi = 96
plt.figure(figsize=(1200 / my_dpi, 600 / my_dpi), dpi=my_dpi).show()


def usage():
    print('use: -n <nodes> -h <hopes>')

def plotRegression(file_name):

    with open(file_name, 'r') as file:
        linear_json = json.loads(file.read())

    x = np.array(linear_json['x'])
    y = np.array(linear_json['y'])

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    popt, pcov = curve_fit(curve_regression, x, y)

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    popt, pcov = curve_fit(curve_regression, x, y, maxfev=1000, check_finite=False)

    f = 'f(x) = %0.4f + %.4f*x; corr=%.4f, p=%.4f, err=%.4f' % (intercept, slope, r_value, p_value, std_err)
    print(f)

    a = popt[0]
    b = popt[1]
    c = popt[2]
    ex = 'f(x): a= %4.f + %.4f*log2(%.4f+x)' % (b, a, c)
    print(ex, '; cov = ', pcov)

    plt.plot(x, y, 'o', label='Measured nodes/tps')
    plt.plot(x, intercept + slope * x, 'r', label=f)

    xdata = np.linspace(x[0], x[-1], 100)
    plt.plot(xdata, curve_regression(xdata, *popt), 'b-', label=ex)

    hps = 'attempts'

    if int(hopes[0]) == 1:
        hps = 'attempt'

    plt.title('Karma Core Benchmark: %s %s per client' % (hopes[0], hps))
    plt.xlabel('count of nodes process transactions ')
    plt.ylabel('transactions per seconds')
    plt.legend()

    plt.show()


def plotAlpha(files, nodes, hopes):

    for i in range(0,len(files)):

        f = files[i]

        with open(f, 'r') as file:
            linear_json = json.loads(file.read())

        x = np.array(linear_json['x'])
        y = np.array(linear_json['y'])

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        popt, pcov = curve_fit(curve_regression, x, y)

        hopes_string = 'attemps count %s' % hopes[i]

        plt.plot(x, intercept + slope * x, label='linear: %s' % hopes_string)

        xdata = np.linspace(x[0], x[-1], 100)
        plt.plot(xdata, curve_regression(xdata, *popt), label='log: %s' % hopes_string)

    plt.title('Karma Core Benchmark: %s nodes' % nodes[0])
    plt.xlabel('count of nodes process transactions ')
    plt.ylabel('transactions per seconds')
    plt.legend()

    plt.show()

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:v,h:v", ["nodes", "hopes"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print
        str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    hopes = []
    nodes = []

    for o, a in opts:
        if o in ("-n", "--nodes"):
            nodes.append(a)
        elif o in ("-h", "--hopes"):
            hopes.append(a)
        else:
            assert False, "unhandled option"

    linear_json = {}

    if len(nodes) > 1:
        if len(nodes) != len(hopes):
            usage()
            sys.exit(2)
        files = []
        for i in range(0,len(nodes)):
            files.append('./linear_h:%s_n:%s.json' % (hopes[i], nodes[i]))
        plotAlpha(files, nodes, hopes)
    else:
        plotRegression('./linear_h:%s_n:%s.json' % (hopes[0], nodes[0]))
