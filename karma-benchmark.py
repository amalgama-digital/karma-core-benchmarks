__author__ = 'denn'


#
# Setup
#

hops = 10

walletPasswd = 'prosto-passwd'
asset = 'KRMT'
amount = '0.01'

from KarmaApi import karma, apis, nodes
from bitshares.block import Block
from bitshares.account import Account

import time
import sys
import threading

karma.wallet.unlock(walletPasswd)

def transactionBilder():

    print(".", end='')
    count = 0
    for n in nodes:
        for i in range(0, hops):
            trx = karma.transferTrx(n['from'], amount, asset, account=n['to']).json()
            n['trx'].append(trx)
            print(".", end='')
            sys.stdout.flush()
            count += 1

    return  count

def transactionExec(transactions, api):
    for trx in transactions:
        print('send trx to node: ', api.rpc.url)
        api.rpc.broadcast_transaction(trx, api='network_broadcast')

def startTransaction():
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

def runBench():
    #
    # Test trx time
    #
    print('Trx building', end='')
    t0 = time.time()
    count = transactionBilder()
    t1 = time.time()
    print('done')

    print('Trx execution...', end='')
    sys.stdout.flush()
    t2 = time.time()
    startTransaction()
    t3 = time.time()
    print('done')

    print('Transaction build time:     ', '%2.3f' % (t1-t0), 'sec.; rate: ', '%2.3f' % (count/(t1-t0)), 'tps')
    print('Transaction execution time: ', '%2.3f' % (t3-t2), 'sec.; rate: ', '%2.3f' % (count/(t3-t2)), 'tps')


if __name__ == '__main__':
    runBench()
    testUserAccount()