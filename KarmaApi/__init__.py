__author__ = 'denn'

from bitsharesbase.chains import known_chains
from graphenebase.base58 import known_prefixes
import np
import time

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

urls = ['ws://localhost']

ports = [8090, 8091, 8092, 8093, 8094, 8095, 8096, 8097, 8098, 8099,
         8190, 8191, 8192, 8193, 8194, 8195, 8196, 8197, 8198, 8199]

accounts = ['bench-mark', 'bench-mark1', 'bench-mark2',
            'bench-mark3', 'bench-mark10',
            'bench-mark11', 'bench-mark12',
            'bench-mark13']

def makeNodes(count):
    np.random.seed(int(time.time()))

    nodes = []
    for i in range(0,count):
        url = urls[int(np.random.randint(len(urls)))]
        port = ports[np.random.randint(len(ports))]
        url = '%s:%s' % (url, port)
        _from = accounts[int(np.random.randint(len(accounts)))]
        _to = accounts[int(np.random.randint(len(accounts)))]
        while _to == _from:
            _to = accounts[int(np.random.randint(len(accounts)))]

        n = {'url': url, 'from': _from, 'to': _to, 'trx': []}
        nodes.append(n)

    return nodes


def curve_regression(x, a, b, c):
    return a*np.log2(c+x)+b

#base_node = nodes[0]['url']

#
# curl -X POST -H "Content-Type: application/json" -d '{"method":"call","params":[0,"get_chain_properties",[]],"id":1}' "https://testnet-node.karma.red"
# curl -X POST -H "Content-Type: application/json" -d '{"method":"call","params":["history","get_account_history",["1.2.91", "1.11.0", 1, "1.11.999999999"]],"id":1}' "https://testnet-node.karma.red"
#
