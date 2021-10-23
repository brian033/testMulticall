from web3 import Web3

w3ws = Web3(Web3.WebsocketProvider('wss://api.avax.network/ext/bc/C/ws'))
from web3.middleware import geth_poa_middleware
w3ws.middleware_onion.inject(geth_poa_middleware, layer=0)


rpc_url = "https://api.avax.network/ext/bc/C/rpc"

w3 = Web3(Web3.HTTPProvider(rpc_url))

netWorkId = w3.eth.chainId
print(f"Web3 connection status: {w3.isConnected()} on network: {netWorkId}")