__author__ = 'denn'

from bitshares import BitShares
from bitsharesbase.chains import known_chains
from graphenebase.base58 import known_prefixes

known_prefixes.append('KRM')
known_prefixes.append('KRMT')
known_prefixes.append('KRMD')

known_chains['Karma'] = {}
known_chains['Karma']['core_symbol']='KRM'
known_chains['Karma']['prefix']='KRM'
known_chains['Karma']['chain_id']='c85b4a30545e09c01aaa7943be89e9785481c1e7bd5ee7d176cb2b3d8dd71a70'

known_chains['KarmaTest'] = {}
known_chains['KarmaTest']['core_symbol']='KRMT'
known_chains['KarmaTest']['prefix']='KRMT'
known_chains['KarmaTest']['chain_id']='e81bea67cebfe8612010fc7c26702bce10dc53f05c57ee6d5b720bbe62e51bef'

#nodes = ['wss://testnet-node.karma.red/','ws://localhost:8090/']
nodes = ['ws://localhost:8090/']
base_node = nodes[0]

wif = '5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3'
karma = BitShares(base_node,nobroadcast=False, expiration=30000)
karma.config.config_defaults['node']=base_node

apis = []

for n in nodes:
    bts = BitShares(n, nobroadcast=False, expiration=30000)
    #karma.config.config_defaults['node']=n
    apis.append(bts)


#
# curl -X POST -H "Content-Type: application/json" -d '{"method":"call","params":[0,"get_chain_properties",[]],"id":1}' "https://testnet-node.karma.red"
# curl -X POST -H "Content-Type: application/json" -d '{"method":"call","params":["history","get_account_history",["1.2.91", "1.11.0", 1, "1.11.999999999"]],"id":1}' "https://testnet-node.karma.red"
#
