__author__ = 'denn'


import requests
import json

def main():
    url = "https://testnet-node.karma.red/rpc"
    headers = {'content-type': 'application/json'}

    payload = {'method': 'call', 'params': ['history', 'get_account_history', ['1.2.91', '1.11.0', 100, '1.11.9999999998']], 'jsonrpc': '2.0', 'id': 7}


    payload2 = {'method': 'call',
               'params': [0, 'get_required_fees',
                          [[[5,
                             {'fee': {'amount': 0, 'asset_id': '1.3.0'},
                              'registrar': '1.2.6',
                              'referrer': '1.2.6',
                              'referrer_percent': 1000,
                              'name': 'bench-mark3',
                              'owner': {'weight_threshold': 1,
                                        'account_auths': [],
                                        'key_auths': [['KRMT4w3noHJ6vM6PVYeeFmo4tSPDsNdqa2rpzG552uxwSPuv5oQ6Uu', '1']],
                                        'extensions': []},
                              'active': {'weight_threshold': 1,
                                         'account_auths': [],
                                         'key_auths': [['KRMT4w3noHJ6vM6PVYeeFmo4tSPDsNdqa2rpzG552uxwSPuv5oQ6Uu', '1']],
                                         'extensions': []},
                              'options': {'memo_key': 'KRMT4w3noHJ6vM6PVYeeFmo4tSPDsNdqa2rpzG552uxwSPuv5oQ6Uu',
                                          'voting_account': '1.2.5',
                                          'num_witness': 0,
                                          'num_committee': 0,
                                          'votes': [],
                                          'extensions': []},
                              'extensions': {}}]],
                           '1.3.0']],
               'jsonrpc': '2.0', 'id': 9
            }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print("response = ", response)

if __name__=='__main__':
    main()