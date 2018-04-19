__author__ = 'denn'

from KarmaApi import makeNodes, curve_regression
from bitshares.block import Block
from bitshares.account import Account
from bitshares import BitShares
from bitsharesbase.account import PrivateKey, PasswordKey

import time
import sys
import threading
import traceback
import json

#
# Setup
#


srcHopes = 20

srcNodes = makeNodes(50)

walletPasswd = 'prosto-passwd'
asset = 'KRMT'
amount = '0.01'

#
# Utils
#

def transactionBilder(nodes):
    apis = {}

    print(".", end='')
    count = 0
    hops = int(srcHopes / len(nodes))

    if hops <= 0:
        hops = 1

    for n in nodes:
        api = BitShares(n['url'], nobroadcast=False, expiration=30000)
        apis[n['url']] = api
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

    return apis, count

def transactionExec(transactions, api):

    for trx in transactions:

        try:
            api.rpc.broadcast_transaction(trx, api='network_broadcast')
        except Exception as err:
            traceback.print_tb(err.__traceback__, err)

        print(".", end='')
        sys.stdout.flush()


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

    #
    # Test trx time
    #
    print('Trx building', end='')
    t0 = time.time()
    apis, count = transactionBilder(nodes)
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

if __name__ == '__main__':

    n = len(srcNodes)
    q = Queue()

    for count in range(1, n+1):
        p = Process(target=runBench, args=(count, q,))
        p.start()
        p.join()

    x = []
    y = []

    while not q.empty():
        p = q.get_nowait()
        x.append(p['x'])
        y.append(p['y'])

    linear_file_name = './linear_h:%s_n:%s.json' % (srcHopes, len(srcNodes))

    linear_json = '{"x": %s, "y": %s}' % (json.dumps(x), json.dumps(y))

    with open(linear_file_name, 'w') as file:
        file.write(linear_json)
