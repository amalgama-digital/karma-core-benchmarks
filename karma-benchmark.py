__author__ = 'denn'

from KarmaApi import nodes as srcNodes
from bitshares.block import Block
from bitshares.account import Account
from bitshares import BitShares
from bitsharesbase.account import PrivateKey, PasswordKey

import time
import sys
import threading
import traceback

#
# Setup
#

srcHops = 50

walletPasswd = 'prosto-passwd'
asset = 'KRMT'
amount = '0.01'

#
# Utils
#

def transactionBilder(apis, nodes):

    print(".", end='')
    count = 0
    hops = int(srcHops / len(nodes))

    if hops <= 0:
        hops = 1

    for n in nodes:
        api = apis[n['url']]
        api.wallet.unlock(walletPasswd)

        try:
            name = n['from']
            wif = PasswordKey(name, walletPasswd, role="active").get_private_key()
            api.wallet.addPrivateKey(wif)
        except:
            pass

        for i in range(0, hops):
            trx = api.transferTrx(n['to'], amount, asset, account=n['from']).json()
            n['trx'].append(trx)
            print(".", end='')
            sys.stdout.flush()
            count += 1

    return count

def transactionExec(transactions, api):

    for trx in transactions:

        try:
            api.rpc.broadcast_transaction(trx, api='network_broadcast')
        except Exception as err:
            traceback.print_tb(err.__traceback__, err)

        print(".", end='')
        sys.stdout.flush()


def createApis(nodes):
    apis = {}

    for n in nodes:
        bts = BitShares(n['url'], nobroadcast=False, expiration=30000)
        print('add node: ', bts.rpc.url)
        apis[n['url']] = bts

    return apis


def startTransaction(apis, nodes):

    threads = []
    for n in nodes:
        api = apis[n['url']]
        t = threading.Thread(target=transactionExec, args=(n['trx'], api, ))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

#
# Test user account
#
def testUserAccount(instance):
    account = Account('bench-mark', bitshares_instance=instance, full=True)
    print(account.balances)
    hist = account.history(limit=10)
    i = 0
    for h in hist:
        block_num = h['block_num']
        trx_in_block = h['trx_in_block']
        ids = h['id']

        block = Block(block_num)
        timestamp = block['timestamp']
        txs       = block['transactions']
        root      = block['transaction_merkle_root']
        witness   = block['witness']

        print('block root: ', root, ' witness: ', witness)
        print('id = ', ids, 'trxs = ', trx_in_block, ' block num = ', block_num, ' block[', timestamp, '] = ', len(txs))

        i += 1

    print('transfers = ', i)

def runBenchFor(nodes):

    apis = createApis(nodes)

    #
    # Test trx time
    #
    print('Trx building', end='')
    t0 = time.time()
    count = transactionBilder(apis, nodes)
    t1 = time.time()
    print('done')


    print('Trx execution', end='')
    sys.stdout.flush()
    t2 = time.time()
    startTransaction(apis, nodes)
    t3 = time.time()
    print('done')

    print('Transaction build time:     ', '%2.3f' % (t1-t0), 'sec.; rate: ', '%2.3f' % (count/(t1-t0)), 'tps')

    tps = (count/(t3-t2))
    n = len(nodes)
    print('Transaction execution time: ', '%2.3f' % (t3-t2), 'sec.; rate: ', '%2.3f' % tps, 'tps', 'nodes count: ', n)

    return tps, n

def runBench(newCount,queue):
    if newCount > 0:
        count = newCount
        nodes = []
        for i in range(0, count):
            nodes.append(srcNodes[i])

        tps, n = runBenchFor(nodes)

        queue.put({'x': n, 'y': tps})


#
# Run test
#

from multiprocessing import Process, Queue
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import np


def func(x, a, b, c):
    return a*np.log2(c+x)+b


if __name__ == '__main__':

    n = len(srcNodes)
    q = Queue()

    for count in range(1, n+1):
        p = Process(target=runBench, args=(count, q,))
        p.start()
        p.join()

    x = []
    y = []
    while q.empty() != True :
        p = q.get_nowait()
        x.append(p['x'])
        y.append(p['y'])

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    x = np.array(x)
    y = np.array(y)


    print(' nodes = ', x, '; tps = ', y, ';')
    f = 'f(x) = %0.4f + %.4f*x; corr=%.4f, p=%.4f, err=%.4f' % (intercept, slope, r_value, p_value, std_err)
    print(f)

    popt, pcov = curve_fit(func, x, y)

    xdata = np.linspace(x[0], x[-1], 100)

    a = popt[0]
    b = popt[1]
    c = popt[2]
    ex = 'f(x): a= %4.f + %.4f*log2(%.4f+x)' % (b, a, c)
    print(ex)

    plt.plot(x, y, 'o', label='Measured nodes/tps')
    plt.plot(x, intercept + slope * x, 'r', label=f)
    plt.plot(xdata, func(xdata, *popt), 'b-', label=ex)

    plt.legend()
    plt.show()
