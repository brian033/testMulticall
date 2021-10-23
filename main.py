from calls import *
from w3Obj import w3, w3ws


multiHttp = getMultiCall(w3)
multiWss = getMultiCall(w3ws)
def avg(ls):
    tt = 0
    for i in ls:
        tt+=i
    return tt/len(ls)


import time
avgtime = {"wss":[],"https":[]}
times = 50
import threading

for i in range(times):
    print("run no." + str(i))
    time_start = time.time() #開始計時
    multiHttp()
    time_end = time.time()    #結束計時
    time_c= time_end - time_start   #執行所花時間
    print('time cost', time_c, 's, using https')
    avgtime["https"].append(time_c)
    time_start = time.time() #開始計時
    multiWss()
    time_end = time.time()    #結束計時
    time_c= time_end - time_start   #執行所花時間
    print('time cost', time_c, 's, using websocket')
    avgtime["wss"].append(time_c)
print(f"over {times} times of testing: ")
print(f"Average time spent on a http call is : {avg(avgtime['https'])}s")
print(f"Average time spent on a wss call is : {avg(avgtime['wss'])}s")
