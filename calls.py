from routes import route
from tokenAddress import tokenContractAddress
from multicallModified.call import Call
from multicallModified.multicall import Multicall
from w3Obj import netWorkId

def getCall(tokenContract, queryAddress):
    return Call(tokenContract, ['balanceOf(address)(uint256)', queryAddress], [None])

def getMultiCall(w3):
    calls = list()
    #uniswapv2 Pools
    for exchange in route:
        #will get PGL and JLP
        for pair in route[exchange]:
            #will get Pair with / between
            pairAddress = route[exchange][pair]
            token1 = pair.split("/")[0]
            token2 = pair.split("/")[1]
            tokenAddr1 = tokenContractAddress[token1]
            tokenAddr2 = tokenContractAddress[token2]
            call1 = Call(tokenAddr1,
                ['balanceOf(address)(uint256)', pairAddress],
                [[f"{exchange}-({pair})_{token1}", None]],
                w3)
            call2 = Call(tokenAddr2,
                ['balanceOf(address)(uint256)', pairAddress],
                [[f"{exchange}-({pair})_{token2}", None]],
                w3)
            calls.append(call1)
            calls.append(call2)

    #curve routes
    # DAI, USDC, USDT, WBTC, WETH代幣編號依序為0-4
    curveVolatileCoins = {'WBTC' : 3, 'ETH' : 4}
    # curveStableCoins = {'DAI': 0, 'USDC' : 1, 'USDT' : 2}
    curveStableCoins = {'USDC' : 1, 'USDT' : 2}
    curvePoolAddr = "0x58e57ca18b7a47112b877e31929798cd3d703b0f"
    for volatileCoin in curveVolatileCoins:
        for stableCoin in curveStableCoins:
            c1 = curveStableCoins[stableCoin]
            c2 = curveVolatileCoins[volatileCoin]
            call1 = Call(curvePoolAddr, 
                ['get_dy_underlying(uint256,uint256,uint256)(uint256)', c1, c2, 821394], 
                [[f'CurveTest{c1}{c2}', None]],w3
                )
            call2 = Call(curvePoolAddr, 
                ['get_dy_underlying(uint256,uint256,uint256)(uint256)', c2, c1, 821394], 
                [[f'CurveTest{c2}{c1}', None]],w3
                )
            calls.append(call1)
            calls.append(call2)

    multi = Multicall(calls, w3)
    multi.networkId = netWorkId     
    return multi

