__author__ = 'denn'

from KarmaApi import makeNodes
from bitshares.account import Account
from bitshares.instance import set_shared_bitshares_instance
from bitsharesbase.account import PrivateKey, PasswordKey
from bitshares import BitShares

karma = BitShares('ws://192.168.11.10:8090', nobroadcast=False, expiration=30000)

account = Account('karma', bitshares_instance=karma)

for a in account.history():
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
