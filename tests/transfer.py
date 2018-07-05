__author__ = 'denn'

from KarmaApi import makeNodes
from bitshares.block import Block
from bitshares.account import Account
from bitshares import BitShares
from bitsharesbase.account import PrivateKey, PasswordKey

import sys
import json

asset = 'KRMT'
amount = '1'

#
# Utils
#

karma = None

while True:
    passwd = 'prosto-passwd'
    wif = ''
    if not karma:
        wif = input('Enter karma wif: ')
        karma = BitShares('wss://testnet-node.karma.red', nobroadcast=False, expiration=30000)
        #karma = BitShares('ws://localhost:8090', nobroadcast=False, expiration=30000)
        karma.wallet.unlock(passwd)

        memo_key = karma.wallet.getMemoKeyForAccount('karma')

        print(memo_key)

        try:
            karma.wallet.addPrivateKey(wif)
        except Exception as err:
            print(err)
            pass

    name = input('Enter recipient: ')
    account = Account(name, bitshares_instance=karma, full=True)
    #m = 'Чувак! Ты типа как бы стал победителем лови сюда карма токенов: %s' % amount
    m = 'Dude! You have got some money %s from Karma!' % amount
    trx = karma.transferTrx(account, amount, asset, account='karma', memo='%s' % m).json()

    karma.rpc.broadcast_transaction(trx, api='network_broadcast')

    print(trx)

    text = str(input('Quit: yes/no?'))
    if text.startswith('quit') or text.startswith('y'):
        sys.exit(0)

    print(text)