__author__ = 'denn'

from KarmaApi import nodes as srcNodes
from bitshares.block import Block
from bitshares.account import Account
from bitshares import BitShares

import time
import sys
import threading
import traceback

#
# Setup
#

srcHops = 10

walletPasswd = 'prosto-passwd'
asset = 'KRMT'
amount = '0.01'

def transactionBilder(apis, nodes):

    print(".", end='')
    count = 0
    hops = int(srcHops / len(nodes))

    if hops <= 0:
        hops = 1

    for n in nodes:
        api = apis[n['url']]
        api.wallet.unlock(walletPasswd)
        for i in range(0, hops):
            trx = api.transferTrx(n['to'], amount, asset, account=n['from']).json()
            n['trx'].append(trx)
            print(".", end='')
            sys.stdout.flush()
            count += 1

    return count

def transactionExec(transactions, api):
    for trx in transactions:
        print('send trx to node: ', api.rpc.url)
        try:
            api.rpc.broadcast_transaction(trx, api='network_broadcast')
        except Exception as err:
            traceback.print_tb(err.__traceback__)

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
def testUserAccount():
    account = Account('bench-mark', bitshares_instance=karma, full=True)
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
        print('id = ', ids, 'trxs = ', trx_in_block, ' block num = ', block_num, ' block[',timestamp,'] = ', len(txs))

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


    print('Trx execution...', end='')
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


from multiprocessing import Process, Queue

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

    print(' nodes = ', x, '; tps = ', y, ';')


# hops = 10
# Transaction execution time:  0.016 sec.; rate:  644.861 tps nodes count:  1
# Transaction execution time:  0.016 sec.; rate:  642.717 tps nodes count:  2
# Transaction execution time:  0.015 sec.; rate:  600.635 tps nodes count:  3
# Transaction execution time:  0.012 sec.; rate:  658.279 tps nodes count:  4
# Transaction execution time:  0.018 sec.; rate:  571.361 tps nodes count:  5
# Transaction execution time:  0.007 sec.; rate:  835.158 tps nodes count:  6
# Transaction execution time:  0.008 sec.; rate:  864.423 tps nodes count:  7
# Transaction execution time:  0.010 sec.; rate:  860.826 tps nodes count:  8
# Transaction execution time:  0.010 sec.; rate:  919.602 tps nodes count:  9
# Transaction execution time:  0.012 sec.; rate:  849.410 tps nodes count:  10
# x = [1,2,3,4,5,6,7,8,9,10]; y = [644.861,642.717,600.635,658.279,571.361,835.158,864.423,860.826,919.602,849.410]



