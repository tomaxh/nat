from threading import Thread
from queue import Queue
import requests
import time

NUM_THREAD = 4
REQUEST_INTERVAL = 1
ITERATION = 5

result = Queue() 

class MyThread (Thread):
    def run(self):
        i = 0
        while i < ITERATION:
            t = time.time()
            requests.get("http://tree.lass.leg.bc.ca/nat-api/search?s=canada")
            d = time.time()-t
            result.put(d)
            time.sleep(REQUEST_INTERVAL)
            i += 1

threads = []
for i in range(NUM_THREAD):
    threads.append(MyThread())

for thread in threads:
    thread.start()

resultL = []
total = NUM_THREAD*ITERATION
while len(resultL) < total:
    resultL.append(result.get())
    print(''.join((
        '\r|', 
        '%'*len(resultL), ' '*(total - len(resultL)), 
        '| (%.2f %%, Avg: %.2f)'%(
            len(resultL)*100/total, sum(resultL)/len(resultL)
    ))), end='')

print()
print('Avg: ', sum(resultL)/len(resultL), ' | Samples: ', len(resultL))

for thread in threads:
    thread.join()
