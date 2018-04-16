__author__ = 'denn'

import KarmaApi

KarmaApi.karma.wallet.unlock('prosto-passwd')
accounts = KarmaApi.karma.wallet.getAccounts()

for a in accounts:
    print(' account = ', a)
