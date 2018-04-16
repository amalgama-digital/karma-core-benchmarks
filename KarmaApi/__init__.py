__author__ = 'denn'

from bitsharesbase.chains import known_chains
from graphenebase.base58 import known_prefixes

known_prefixes.append('KRM')
known_prefixes.append('KRMT')
known_prefixes.append('KRMD')

known_chains['Karma'] = {}
known_chains['Karma']['core_symbol'] = 'KRM'
known_chains['Karma']['prefix'] = 'KRM'
known_chains['Karma']['chain_id'] = 'c85b4a30545e09c01aaa7943be89e9785481c1e7bd5ee7d176cb2b3d8dd71a70'

known_chains['KarmaTest'] = {}
known_chains['KarmaTest']['core_symbol'] = 'KRMT'
known_chains['KarmaTest']['prefix'] = 'KRMT'
known_chains['KarmaTest']['chain_id'] = 'e81bea67cebfe8612010fc7c26702bce10dc53f05c57ee6d5b720bbe62e51bef'

nodes = [
    {'url': 'ws://localhost:8090/', 'from': 'bench-mark10',  'to': 'bench-mark1', 'trx': []}, # 1
    {'url': 'ws://localhost:8091/', 'from': 'bench-mark13',  'to': 'bench-mark1', 'trx': []}, # 2
    {'url': 'ws://localhost:8092/', 'from': 'bench-mark13',  'to': 'bench-mark2', 'trx': []}, # 3
    {'url': 'ws://localhost:8093/', 'from': 'bench-mark12', 'to': 'bench-mark',  'trx': []}, # 4
    {'url': 'ws://localhost:8094/', 'from': 'bench-mark10',  'to': 'bench-mark2', 'trx': []}, # 5
    {'url': 'ws://localhost:8095/', 'from': 'bench-mark13', 'to': 'bench-mark1', 'trx': []}, # 6
    {'url': 'ws://localhost:8096/', 'from': 'bench-mark10',  'to': 'bench-mark1', 'trx': []}, # 7
    {'url': 'ws://localhost:8097/', 'from': 'bench-mark12', 'to': 'bench-mark1', 'trx': []}, # 8
    {'url': 'ws://localhost:8098/', 'from': 'bench-mark13', 'to': 'bench-mark1', 'trx': []}, # 9
    {'url': 'ws://localhost:8099/', 'from': 'bench-mark13', 'to': 'bench-mark2', 'trx': []}, # 10

    {'url': 'ws://localhost:8090/', 'from': 'bench-mark11', 'to': 'bench-mark', 'trx': []},  # 1
    {'url': 'ws://localhost:8091/', 'from': 'bench-mark12', 'to': 'bench-mark1', 'trx': []},  # 2
    {'url': 'ws://localhost:8092/', 'from': 'bench-mark10', 'to': 'bench-mark2', 'trx': []},  # 3
    {'url': 'ws://localhost:8093/', 'from': 'bench-mark12', 'to': 'bench-mark', 'trx': []},  # 4
    {'url': 'ws://localhost:8094/', 'from': 'bench-mark11', 'to': 'bench-mark2', 'trx': []},  # 5
    {'url': 'ws://localhost:8095/', 'from': 'bench-mark13', 'to': 'bench-mark1', 'trx': []},  # 6
    {'url': 'ws://localhost:8096/', 'from': 'bench-mark11', 'to': 'bench-mark3', 'trx': []},  # 7
    {'url': 'ws://localhost:8097/', 'from': 'bench-mark12', 'to': 'bench-mark1', 'trx': []},  # 8
    {'url': 'ws://localhost:8098/', 'from': 'bench-mark13', 'to': 'bench-mark1', 'trx': []},  # 9
    {'url': 'ws://localhost:8099/', 'from': 'bench-mark13', 'to': 'bench-mark2', 'trx': []},  # 10

    {'url': 'ws://localhost:8090/', 'from': 'bench-mark11', 'to': 'bench-mark', 'trx': []},  # 1
    {'url': 'ws://localhost:8091/', 'from': 'bench-mark12', 'to': 'bench-mark1', 'trx': []},  # 2
    {'url': 'ws://localhost:8092/', 'from': 'bench-mark10', 'to': 'bench-mark2', 'trx': []},  # 3
    {'url': 'ws://localhost:8093/', 'from': 'bench-mark12', 'to': 'bench-mark', 'trx': []},  # 4
    {'url': 'ws://localhost:8094/', 'from': 'bench-mark11', 'to': 'bench-mark2', 'trx': []},  # 5
    {'url': 'ws://localhost:8095/', 'from': 'bench-mark13', 'to': 'bench-mark1', 'trx': []},  # 6
    {'url': 'ws://localhost:8096/', 'from': 'bench-mark11', 'to': 'bench-mark3', 'trx': []},  # 7
    {'url': 'ws://localhost:8097/', 'from': 'bench-mark12', 'to': 'bench-mark1', 'trx': []},  # 8
    {'url': 'ws://localhost:8098/', 'from': 'bench-mark13', 'to': 'bench-mark1', 'trx': []},  # 9
    {'url': 'ws://localhost:8099/', 'from': 'bench-mark13', 'to': 'bench-mark2', 'trx': []},  # 10
]

base_node = nodes[0]['url']

#
# curl -X POST -H "Content-Type: application/json" -d '{"method":"call","params":[0,"get_chain_properties",[]],"id":1}' "https://testnet-node.karma.red"
# curl -X POST -H "Content-Type: application/json" -d '{"method":"call","params":["history","get_account_history",["1.2.91", "1.11.0", 1, "1.11.999999999"]],"id":1}' "https://testnet-node.karma.red"
#
