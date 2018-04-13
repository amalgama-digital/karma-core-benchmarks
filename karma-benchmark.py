__author__ = 'denn'


#
# Setup
#

hops         = 20

fromAccount  = 'bench-mark2'
toAccount    = 'bench-mark1'
walletPasswd = 'prosto-passwd'
asset        = 'KRMT'
amount       = '0.001'

from KarmaApi import karma, apis
from bitshares.block import Block
from bitshares.account import Account

import time
import sys


karma.wallet.unlock(walletPasswd)

def transactionBilder():
    transactions = []

    print(".", end='')
    for i in range(0,hops):
        trx=karma.transferTrx(toAccount, amount, asset, account=fromAccount).json()
        transactions.append(trx)
        print(".", end='')
        sys.stdout.flush()

    return transactions

def transactionExec(transactions):
    i = 0
    for trx in transactions:
        k = i % len(apis)
        api = apis[k]
        api.rpc.broadcast_transaction(trx, api='network_broadcast')
        i += 1

#
# Test user account
#
def testUserAccount():
    account = Account(toAccount, bitshares_instance=karma, full=True)
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
    trx = transactionBilder()
    t1 = time.time()
    print('done')

    count = len(trx)

    print('Trx execution...', end='')
    sys.stdout.flush()
    t2 = time.time()
    transactionExec(trx)
    t3 = time.time()
    print('done')

    print('Transaction build time:     ', '%2.3f' % (t1-t0), 'sec.; rate: ', '%2.3f' % (count/(t1-t0)), 'tps')
    print('Transaction execution time: ', '%2.3f' % (t3-t2), 'sec.; rate: ', '%2.3f' % (count/(t3-t2)), 'tps')


if __name__ == '__main__':
    runBench()
    testUserAccount()