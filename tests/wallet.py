__author__ = 'denn'

from KarmaApi import makeNodes
from bitshares import BitShares
from bitsharesbase.account import PrivateKey, PasswordKey

walletPasswd = 'prosto-passwd'
asset = 'KRMT'
amount = 10
karmaAccount = 'karma'

karma = BitShares('wss://testnet-node.karma.red', nobroadcast=False, expiration=30000)
karma.wallet.unlock(walletPasswd)

try:
    name = karmaAccount
    #wif = PasswordKey(name, walletPasswd, role="active").get_private_key()
    wif = '5JHC4d9USEWosKsdcQPc9oGbUArgqtMYyHUE68JGf6bN6PvJ94m'
    karma.wallet.addPrivateKey(wif)
except:
    print('key already added')
    pass

#karma.transfer('airdrop-japan', 425000, asset, account=karmaAccount)

benchAccounts = ['bench-mark', 'bench-mark1', 'bench-mark2', 'bench-mark3',
                 'bench-mark10', 'bench-mark11', 'bench-mark12', 'bench-mark13']

for a in benchAccounts:
    karma.transfer(a, amount, asset, account=karmaAccount)
