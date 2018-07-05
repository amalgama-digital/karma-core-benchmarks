__author__ = 'denn'

from KarmaApi import makeNodes
from bitshares.account import Account
from bitshares.asset import Asset
from bitshares.instance import set_shared_bitshares_instance
from bitsharesbase.account import PrivateKey, PasswordKey
from bitshares import BitShares

#karma = BitShares('ws://localhost:8090', nobroadcast=False, expiration=30000)
karma = BitShares('wss://testnet-node.karma.red', nobroadcast=False, expiration=30000)

account = Account('karma', bitshares_instance=karma)

#asset = Asset('1.3.1', bitshares_instance=karma)

for a in account.history(limit=10):
   print(a)

# core_unit = 'KRMT'
#
# karma.wallet.unlock('prosto-passwd')
#
# name   = 'bench-mark2'
# passwd = 'prosto-passwd'
#
# #active_key = PasswordKey(name, passwd, role="active")
# #memo_key = PasswordKey(name, passwd, role="memo")
# #owner_key = PasswordKey(name, passwd, role="owner")
#
# tx = karma.create_account(
#             name,
#             registrar="karma",   # 1.2.7
#             referrer="init0",    # 1.2.8
#             referrer_percent=10,
#             password=passwd
#         )
#
