#!/usr/bin/env python

#-----------------------------------------------------------------------
# prodcon.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from threading import Thread
from queue import Queue

#-----------------------------------------------------------------------

class ProducerThread (Thread):
    
    def __init__(self, queue):
        Thread.__init__(self)
        self._queue = queue
        
    def run(self):
        for i in range(100):
            self._queue.put(i)
            print('Produced:', i)

#-----------------------------------------------------------------------

class ConsumerThread (Thread):
    
    def __init__(self, queue):
        Thread.__init__(self)
        self._queue = queue
        
    def run(self):
        for i in range(100):
            n = self._queue.get()
            print('Consumed:', n)

#-----------------------------------------------------------------------

def main():
    
    QUEUE_SIZE = 10  # Arbitrary

    queue = Queue(QUEUE_SIZE);
    
    producerThread = ProducerThread(queue)
    consumerThread = ConsumerThread(queue)
    
    producerThread.start()
    consumerThread.start()
    
    producerThread.join()
    consumerThread.join()
    
    print('Finished')

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
